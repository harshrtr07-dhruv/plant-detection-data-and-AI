"""
train.py — Baseline Model Training Script
Phase 3 | Plant Disease Detection System | VIT Bhopal University

Architecture:
    Input (224x224x3, uint8 0-255)
    -> tf.keras.layers.Rescaling(1/127.5, offset=-1)
    -> MobileNetV2 (ImageNet backbone, pre-trained)
    -> GlobalAveragePooling2D()
    -> Dropout(0.3)
    -> Dense(num_classes, activation="softmax")

Training Scheme:
    Round 1: Frozen backbone, Adam lr=1e-3, EarlyStopping (patience=3)
    Round 2: Fine-tune top 30 layers, Adam lr=1e-5, ReduceLROnPlateau, EarlyStopping
"""

import argparse
import csv
import json
import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import classification_report, f1_score


def parse_args():
    parser = argparse.ArgumentParser(description="Train Plant Disease Detection Baseline")
    parser.add_argument("--train-csv", type=str, default="data/splits/train.csv", help="Path to train CSV")
    parser.add_argument("--val-csv", type=str, default="data/splits/val.csv", help="Path to validation CSV")
    parser.add_argument("--models-dir", type=str, default="models", help="Directory to save model artifacts")
    parser.add_argument("--docs-dir", type=str, default="docs", help="Directory to save training curves & logs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--epochs-r1", type=int, default=10, help="Epochs for Round 1 (frozen backbone)")
    parser.add_argument("--epochs-r2", type=int, default=15, help="Epochs for Round 2 (fine-tuning)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args()


def load_data(train_csv_path, val_csv_path):
    train_df = pd.read_csv(train_csv_path)
    val_df = pd.read_csv(val_csv_path)

    classes = sorted(train_df["label"].unique())
    class_to_idx = {name: idx for idx, name in enumerate(classes)}
    idx_to_class = {idx: name for idx, name in enumerate(classes)}

    train_df["target"] = train_df["label"].map(class_to_idx)
    val_df["target"] = val_df["label"].map(class_to_idx)

    return train_df, val_df, class_to_idx, idx_to_class


def build_dataset(df, batch_size=32, is_training=True, seed=42):
    paths = df["path"].values
    labels = df["target"].values

    def parse_image(path, label):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, [224, 224])
        # Keep pixel values at 0-255 float; Rescaling layer inside model handles normalization
        return image, label

    dataset = tf.data.Dataset.from_tensor_slices((paths, labels))
    if is_training:
        dataset = dataset.shuffle(buffer_size=len(df), seed=seed)

    dataset = dataset.map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    return dataset


def build_data_augmentation():
    return tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.08),  # approx 15-20 degrees
        tf.keras.layers.RandomZoom(0.15),
        tf.keras.layers.RandomContrast(0.15),
    ], name="data_augmentation")


def build_model(num_classes):
    inputs = tf.keras.Input(shape=(224, 224, 3), name="input_image")

    # Built-in normalization: scales [0, 255] to [-1, 1] as expected by MobileNetV2
    x = tf.keras.layers.Rescaling(1.0 / 127.5, offset=-1.0, name="rescaling")(inputs)

    # Base pre-trained backbone
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D(name="avg_pool")(x)
    x = tf.keras.layers.Dropout(0.3, name="top_dropout")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="plant_disease_mobilenetv2")
    return model, base_model


def compute_class_weights(train_df):
    class_counts = train_df["target"].value_counts().to_dict()
    total_samples = len(train_df)
    num_classes = len(class_counts)
    class_weights = {
        cls: total_samples / (num_classes * count)
        for cls, count in class_counts.items()
    }
    return class_weights


def plot_curves(history_r1, history_r2, out_path):
    acc = history_r1.history["accuracy"] + history_r2.history["accuracy"]
    val_acc = history_r1.history["val_accuracy"] + history_r2.history["val_accuracy"]
    loss = history_r1.history["loss"] + history_r2.history["loss"]
    val_loss = history_r1.history["val_loss"] + history_r2.history["val_loss"]

    epochs_r1_len = len(history_r1.history["accuracy"])

    plt.figure(figsize=(14, 5))

    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(acc, label="Training Accuracy", color="#1f77b4")
    plt.plot(val_acc, label="Validation Accuracy", color="#ff7f0e")
    plt.axvline(x=epochs_r1_len - 1, color="gray", linestyle="--", label="Start Fine-Tuning")
    plt.title("Training and Validation Accuracy", fontsize=12, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)

    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(loss, label="Training Loss", color="#1f77b4")
    plt.plot(val_loss, label="Validation Loss", color="#ff7f0e")
    plt.axvline(x=epochs_r1_len - 1, color="gray", linestyle="--", label="Start Fine-Tuning")
    plt.title("Training and Validation Loss", fontsize=12, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Training curves saved to: {out_path}")


def log_experiment(docs_dir, entry):
    log_file = Path(docs_dir) / "experiment_log.csv"
    file_exists = log_file.exists()

    fieldnames = [
        "run_id", "timestamp", "backbone", "image_size", "batch_size",
        "epochs_round1", "epochs_round2", "optimizer", "lr_round1", "lr_round2",
        "val_accuracy", "val_loss", "val_macro_f1", "model_path", "notes"
    ]

    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)
    print(f"✅ Experiment logged in: {log_file}")


def main():
    args = parse_args()
    tf.random.set_seed(args.seed)
    np.random.seed(args.seed)

    models_dir = Path(args.models_dir)
    docs_dir = Path(args.docs_dir)
    models_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("🌿 Plant Disease Detection — Phase 3 Baseline Model Training")
    print("=" * 60)

    # 1. Load splits
    if not Path(args.train_csv).exists() or not Path(args.val_csv).exists():
        raise FileNotFoundError(
            f"Splits not found at {args.train_csv} or {args.val_csv}. "
            "Please ensure Phase 2 splits are generated before training."
        )

    print(f"Loading data from: {args.train_csv} and {args.val_csv}")
    train_df, val_df, class_to_idx, idx_to_class = load_data(args.train_csv, args.val_csv)
    num_classes = len(class_to_idx)
    print(f"Classes ({num_classes}): {list(class_to_idx.keys())[:5]}... (truncated)")
    print(f"Train samples: {len(train_df):,} | Val samples: {len(val_df):,}")

    # Save labels.json
    labels_path = models_dir / "labels.json"
    with open(labels_path, "w", encoding="utf-8") as f:
        json.dump(idx_to_class, f, indent=2)
    print(f"✅ Class labels mapping saved to: {labels_path}")

    # 2. Build Datasets
    train_ds = build_dataset(train_df, batch_size=args.batch_size, is_training=True, seed=args.seed)
    val_ds = build_dataset(val_df, batch_size=args.batch_size, is_training=False, seed=args.seed)

    # 3. Model Architecture
    model, base_model = build_model(num_classes)
    model.summary()

    # Class weights for handling any data imbalance
    class_weights = compute_class_weights(train_df)

    # 4. Round 1: Frozen Backbone
    print("\n--- ROUND 1: Training Classification Head (Backbone Frozen) ---")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    best_model_path = models_dir / "plant_model_v1.keras"
    callbacks_r1 = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
            verbose=1
        )
    ]

    history_r1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs_r1,
        class_weight=class_weights,
        callbacks=callbacks_r1
    )

    # 5. Round 2: Fine-Tuning Top 30 Layers
    print("\n--- ROUND 2: Fine-Tuning Top 30 Backbone Layers ---")
    base_model.trainable = True
    # Freeze all layers except the last 30
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    trainable_count = sum(np.prod(v.get_shape()) for v in model.trainable_weights)
    print(f"Trainable parameters after unfreezing top 30: {trainable_count:,}")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    callbacks_r2 = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=2,
            min_lr=1e-7,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(best_model_path),
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        )
    ]

    history_r2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs_r2,
        class_weight=class_weights,
        callbacks=callbacks_r2
    )

    # 6. Evaluation on Validation Set
    print("\n--- Evaluating Best Model on Validation Set ---")
    best_model = tf.keras.models.load_model(str(best_model_path))

    val_preds_probs = best_model.predict(val_ds)
    val_preds = np.argmax(val_preds_probs, axis=1)
    val_true = val_df["target"].values

    macro_f1 = f1_score(val_true, val_preds, average="macro")
    final_val_loss, final_val_acc = best_model.evaluate(val_ds, verbose=0)

    print(f"Final Validation Loss     : {final_val_loss:.4f}")
    print(f"Final Validation Accuracy : {final_val_acc:.4f}")
    print(f"Validation Macro F1 Score : {macro_f1:.4f}")

    # Plot & Save curves
    curves_path = docs_dir / "training_curves.png"
    plot_curves(history_r1, history_r2, curves_path)

    # 7. Experiment Log
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    experiment_entry = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "backbone": "MobileNetV2",
        "image_size": "224x224",
        "batch_size": args.batch_size,
        "epochs_round1": len(history_r1.history["accuracy"]),
        "epochs_round2": len(history_r2.history["accuracy"]),
        "optimizer": "Adam",
        "lr_round1": "1e-3",
        "lr_round2": "1e-5",
        "val_accuracy": round(float(final_val_acc), 4),
        "val_loss": round(float(final_val_loss), 4),
        "val_macro_f1": round(float(macro_f1), 4),
        "model_path": str(best_model_path),
        "notes": "Round 1 frozen, Round 2 top-30 unfreeze with ReduceLROnPlateau & class weights"
    }
    log_experiment(docs_dir, experiment_entry)

    print("\n" + "=" * 60)
    print("🎉 Phase 3 Training Completed Successfully!")
    print(f"Model saved to: {best_model_path}")
    print(f"Labels saved to: {labels_path}")
    print(f"Curves saved to: {curves_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()

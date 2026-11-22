"""
kb_validator.py — Knowledge Base Validator
Phase 6 | Plant Disease Detection System | VIT Bhopal University

Usage:
    python src/engine/kb_validator.py

Checks:
  1. Every class in labels.json has a KB entry
  2. No required fields are missing or still say FILL_IN
  3. Every chemical option has a source
  4. reviewed_by and reviewed_on are filled (not PENDING)
  5. At least one source per entry
"""

import json
import os
from pathlib import Path

KB_DIR     = Path("knowledge_base")
LABELS_FILE = Path("models/labels.json")   # generated in Phase 3

REQUIRED_FIELDS = [
    "class_name", "crop", "disease", "is_healthy", "cause_type",
    "spread_risk", "symptoms", "organic_options", "chemical_options",
    "pruning_advice", "watering_advice", "soil_care", "prevention",
    "stage_advice", "sources", "reviewed_by", "reviewed_on", "last_updated"
]

STAGE_KEYS = ["seedling", "vegetative", "flowering", "fruiting"]


def load_labels():
    if not LABELS_FILE.exists():
        print(f"⚠️  {LABELS_FILE} not found — skipping class coverage check (run after Phase 3)")
        return None
    with open(LABELS_FILE) as f:
        return json.load(f)   # expects {index: class_name} or [class_name, ...]


def validate_entry(data: dict, filename: str) -> list:
    errors = []

    # Required fields present
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"  ❌ Missing field: '{field}'")
        elif isinstance(data[field], str) and "FILL_IN" in data[field]:
            errors.append(f"  ❌ Field '{field}' still contains FILL_IN placeholder")
        elif isinstance(data[field], list):
            for i, item in enumerate(data[field]):
                if isinstance(item, str) and "FILL_IN" in item:
                    errors.append(f"  ❌ '{field}[{i}]' still contains FILL_IN placeholder")
                elif isinstance(item, dict):
                    for k, v in item.items():
                        if isinstance(v, str) and "FILL_IN" in v:
                            errors.append(f"  ❌ '{field}[{i}].{k}' still contains FILL_IN")

    # Stage advice keys
    if "stage_advice" in data and isinstance(data["stage_advice"], dict):
        for key in STAGE_KEYS:
            if key not in data["stage_advice"]:
                errors.append(f"  ❌ stage_advice missing key: '{key}'")
            elif "FILL_IN" in str(data["stage_advice"].get(key, "")):
                errors.append(f"  ❌ stage_advice.{key} still contains FILL_IN")

    # Chemical options must have source
    for i, chem in enumerate(data.get("chemical_options", [])):
        if not chem.get("source") or "FILL_IN" in chem.get("source", ""):
            errors.append(f"  ❌ chemical_options[{i}] missing or incomplete 'source'")

    # Must have at least one source
    if not data.get("sources"):
        errors.append("  ❌ 'sources' list is empty")

    # Reviewed
    if data.get("reviewed_by", "").upper() in ("", "PENDING", "PENDING — SUBMIT TO DR. JAGRITI GUPTA"):
        errors.append("  ⚠️  reviewed_by is PENDING — needs agronomist sign-off")
    if data.get("reviewed_on", "").upper() in ("", "PENDING"):
        errors.append("  ⚠️  reviewed_on is PENDING")

    return errors


def main():
    labels = load_labels()
    all_files = list(KB_DIR.glob("*.json"))
    all_files = [f for f in all_files if f.name not in ("schema.json",)]

    print(f"\n{'='*60}")
    print(f"  Knowledge Base Validator")
    print(f"  {len(all_files)} entry files found in {KB_DIR}/")
    print(f"{'='*60}\n")

    # Check coverage against labels.json
    if labels is not None:
        label_values = list(labels.values()) if isinstance(labels, dict) else labels
        kb_classes = {f.stem for f in all_files}
        missing = [l for l in label_values if l not in kb_classes]
        if missing:
            print(f"❌ MISSING KB ENTRIES for {len(missing)} classes:")
            for m in missing:
                print(f"   - {m}")
        else:
            print(f"✅ All {len(label_values)} classes from labels.json have a KB entry\n")

    # Validate each file
    errors_total = 0
    warnings_total = 0
    pending_review = []

    for json_file in sorted(all_files):
        try:
            with open(json_file) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ {json_file.name}: INVALID JSON — {e}\n")
            errors_total += 1
            continue

        errs = validate_entry(data, json_file.name)
        hard_errors = [e for e in errs if "❌" in e]
        warnings    = [e for e in errs if "⚠️" in e]

        if hard_errors:
            print(f"❌ {json_file.stem}")
            for e in hard_errors:
                print(e)
            print()
            errors_total += len(hard_errors)
        elif warnings:
            print(f"⚠️  {json_file.stem} — needs review")
            warnings_total += len(warnings)
            pending_review.append(json_file.stem)
        else:
            print(f"✅ {json_file.stem}")

    print(f"\n{'='*60}")
    print(f"  Results")
    print(f"{'='*60}")
    print(f"  Hard errors  : {errors_total}")
    print(f"  Needs review : {warnings_total} files")
    print(f"  Clean        : {len(all_files) - errors_total - len(pending_review)}")
    if pending_review:
        print(f"\n  Files awaiting review by Dr. Jagriti Gupta:")
        for name in pending_review:
            print(f"    - {name}")
    print()


if __name__ == "__main__":
    main()

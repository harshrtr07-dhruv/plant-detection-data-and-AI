# 🌿 Plant Disease Detection System Using AI

**Project:** Plant Disease Detection System Using AI  
**Institution:** VIT Bhopal University  
**Supervisor:** Dr. Jagriti Gupta  

---

## 📌 Project Overview

This system allows farmers to upload a photo of a plant leaf along with the crop name and growth stage. It then:

1. Preprocesses the image (resize to 224×224, normalize)
2. Runs it through a CNN (MobileNetV2) trained on PlantVillage data
3. Returns the predicted disease and confidence score
4. Estimates disease severity (Low / Medium / High)
5. Looks up a cure plan from a knowledge base
6. Returns everything as a single JSON response

```
Photo + crop + growth_stage
        ↓
   Preprocessing (resize 224×224)
        ↓
    CNN Model (MobileNetV2 / TFLite)
        ↓
   Disease Name + Confidence Score
        ↓
   Severity Estimate (OpenCV-based)
        ↓
  Knowledge-Base Lookup (JSON/MongoDB)
        ↓
  JSON Response → Node.js Backend → React Frontend
```

---

## 🗂️ Folder Structure

```
plant-disease-detection/
│
├── data/                  # Raw and processed datasets, CSV splits
├── notebooks/             # Jupyter / Colab notebooks for EDA and training
├── src/
│   ├── data/              # Data loading, preprocessing, augmentation scripts
│   ├── model/             # Model architecture, training scripts
│   └── engine/            # Severity grading, results engine logic
├── knowledge_base/        # JSON files: disease → cure plan entries
├── service/               # Flask API service (app.py, routes)
├── models/                # Saved trained models (.keras, .tflite, labels.json)
├── docs/                  # API contract, decision log, data card, model card
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Model Training | TensorFlow / Keras (Google Colab) |
| CNN Backbone | MobileNetV2 (ImageNet weights, fine-tuned) |
| Model Serving | TFLite + ai-edge-litert |
| API Service | Flask (Python) |
| Database | MongoDB (via pymongo) |
| Deployment | Render (free tier) / Google Cloud Run (backup) |
| Frontend | React (separate team) |
| Backend API | Node.js (separate team) |

---

## 🚀 Fast Path to a Live Model

1. Complete Phases 1–5 (setup → model v1)
2. Build Phase 8 (Flask service, disease-only version)
3. Complete Phase 9 (export + deploy to Render)
4. Website can then call a **real live model**
5. Phases 6 & 7 (cure content + severity) add on top — **no website changes needed**

---

## 🔗 API Contract

The `/predict` endpoint accepts:
- `image` — leaf photo (multipart, max 5 MB, JPEG/PNG)
- `crop` — crop name (e.g. "tomato", "potato")
- `growth_stage` — one of: `seedling`, `vegetative`, `flowering`, `fruiting`

See `docs/api_contract.md` for the full request/response format.

---

## ⚠️ Known Data Gap

PlantVillage (primary dataset) **does not include** rice, wheat, cotton, or sugarcane — crops critical for Indian farmers. These will be added in Phase 10 from other public datasets (after licence checks).

---

## 👥 Team

| Role | Responsibility |
|------|---------------|
| Data & AI Team | Dataset, model training, Flask service (this repo) |
| Backend Team | Node.js API, user accounts, DB integration |
| Frontend Team | React web app |

---

## 📋 Setup Instructions

```bash
# Clone the repo
git clone <repo-url>
cd plant-disease-detection

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 📄 Licence

Dataset: PlantVillage (Creative Commons CC-BY 4.0)  
Code: MIT License

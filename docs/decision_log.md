# 📋 Decision Log
**Project:** Plant Disease Detection System Using AI  
**Institution:** VIT Bhopal University | **Supervisor:** Dr. Jagriti Gupta  
**Last Updated:** 2026-11-23

> Fill in the "Team Choice" column and get sign-off from all members before writing any code.

---

## 🔧 Technical Decisions

| # | Decision | Options | Team Choice | Reason | Decided By | Date |
|---|----------|---------|-------------|--------|------------|------|
| 1 | CNN Backbone | MobileNetV2 / EfficientNetB0 / ResNet50 | _TBD_ | | | |
| 2 | Training Platform | Google Colab / Kaggle | _TBD_ | | | |
| 3 | Deployment Platform | Render (free) / Google Cloud Run | _TBD_ | | | |
| 4 | Database | MongoDB Atlas / Local JSON | _TBD_ | | | |
| 5 | Image Input Size | 224×224 / 256×256 | 224×224 | Required by MobileNetV2 | Plan doc | 2026-11-23 |
| 6 | Confidence Threshold | 0.60 / 0.70 / 0.80 | 0.70 (starting) | To be tuned from confidence plot in Phase 4 | Plan doc | 2026-11-23 |
| 7 | Pixel Scaling | Inside model (Rescaling layer) | Inside model | Ensures TFLite export carries its own preprocessing | Plan doc | 2026-11-23 |
| 8 | Batch Size | 16 / 32 / 64 | 32 | Standard for MobileNetV2 on Colab GPU | Plan doc | 2026-11-23 |
| 9 | Train/Val/Test Split | 70/15/15 | 70/15/15 | Per-class stratified with seed 42 | Plan doc | 2026-11-23 |
| 10 | Random Seed | 42 | 42 | Fixed for reproducibility across all runs | Plan doc | 2026-11-23 |

---

## 🌾 Dataset Decisions

| # | Decision | Options | Team Choice | Reason | Decided By | Date |
|---|----------|---------|-------------|--------|------------|------|
| 11 | Primary Dataset | PlantVillage (colour / segmented / grayscale) | Colour version | Best for transfer learning | Plan doc | 2026-11-23 |
| 12 | Indian Crop Gap | Add rice/wheat/cotton/sugarcane now or Phase 2 | Phase 2 | PlantVillage has none; find licensed datasets later | Plan doc | 2026-11-23 |
| 13 | Field Test Set | PlantDoc / own photos | _TBD_ | Must NOT be used in training | | |
| 14 | Duplicate removal method | File hash + perceptual hash (imagehash) | Both | Catches exact and near-duplicates | Plan doc | 2026-11-23 |

---

## 🚀 Deployment Decisions

| # | Decision | Options | Team Choice | Reason | Decided By | Date |
|---|----------|---------|-------------|--------|------------|------|
| 15 | Model format for serving | .keras / .tflite | .tflite | Lightweight; ai-edge-litert is much smaller than full TF | Plan doc | 2026-11-23 |
| 16 | Model URL storage | Hardcoded / Environment variable | Env var `MODEL_API_URL` | Keeps URL private, avoids CORS issues | Plan doc | 2026-11-23 |
| 17 | Who calls model service | React frontend / Node.js backend | Node.js backend | Security + avoids browser CORS problems | Plan doc | 2026-11-23 |
| 18 | Max image upload size | 2MB / 5MB / 10MB | 5MB | Balance between quality and server memory | Plan doc | 2026-11-23 |
| 19 | Allowed image formats | JPEG only / JPEG + PNG | JPEG + PNG | Common phone photo formats | Plan doc | 2026-11-23 |

---

## ⚠️ Known Gaps & Notes

- **Indian crop gap:** PlantVillage has **no rice, wheat, cotton or sugarcane**. These are critical for Indian farmers and will be added in **Phase 10** from other public datasets. Candidate datasets to check:
  - iCrop dataset
  - Kaggle rice disease datasets
  - ICAR-published image sets
  - ⚠️ Check licence before using any

- **Free hosting behaviour (Render):** Sleeps after ~15 min of no traffic; takes ~60 sec to wake. Keep model inside the repo — never download at startup. Open `/health` before demos.

- **Lab-to-field gap:** PlantVillage test accuracy will likely be >95% but real-world field accuracy will be lower. This gap must be measured honestly and reported.

---

## ✅ Sign-off

| Team Member | Role | Signed Off | Date |
|-------------|------|-----------|------|
| | Data & AI | ☐ | |
| | Backend (Node.js) | ☐ | |
| | Frontend (React) | ☐ | |
| Dr. Jagriti Gupta | Supervisor | ☐ | |

# 📊 Data Card — PlantVillage Dataset
**Project:** Plant Disease Detection System Using AI  
**Institution:** VIT Bhopal University | **Supervisor:** Dr. Jagriti Gupta  
**Last Updated:** 2026-11-23

---

## Source & Licence
| Field | Value |
|-------|-------|
| **Dataset** | PlantVillage |
| **Source URL** | https://www.kaggle.com/datasets/emmarex/plantdisease |
| **Licence** | Creative Commons CC-BY 4.0 |
| **Download Date** | *(fill in when downloaded)* |
| **Version Used** | Colour (RGB) — NOT segmented or grayscale |

---

## Class List & Image Counts
*(Fill in after Step 2.2 — run `notebooks/01_eda.ipynb`)*

| # | Class Name | Raw Count | After Cleaning |
|---|-----------|-----------|----------------|
| 1 | Apple___Apple_scab | | |
| 2 | Apple___Black_rot | | |
| 3 | Apple___Cedar_apple_rust | | |
| 4 | Apple___healthy | | |
| 5 | Blueberry___healthy | | |
| 6 | Cherry___healthy | | |
| 7 | Cherry___Powdery_mildew | | |
| 8 | Corn___Cercospora_leaf_spot | | |
| 9 | Corn___Common_rust | | |
| 10 | Corn___healthy | | |
| 11 | Corn___Northern_Leaf_Blight | | |
| 12 | Grape___Black_rot | | |
| 13 | Grape___Esca_(Black_Measles) | | |
| 14 | Grape___healthy | | |
| 15 | Grape___Leaf_blight | | |
| 16 | Orange___Haunglongbing | | |
| 17 | Peach___Bacterial_spot | | |
| 18 | Peach___healthy | | |
| 19 | Pepper___Bacterial_spot | | |
| 20 | Pepper___healthy | | |
| 21 | Potato___Early_blight | | |
| 22 | Potato___healthy | | |
| 23 | Potato___Late_blight | | |
| 24 | Raspberry___healthy | | |
| 25 | Soybean___healthy | | |
| 26 | Squash___Powdery_mildew | | |
| 27 | Strawberry___healthy | | |
| 28 | Strawberry___Leaf_scorch | | |
| 29 | Tomato___Bacterial_spot | | |
| 30 | Tomato___Early_blight | | |
| 31 | Tomato___healthy | | |
| 32 | Tomato___Late_blight | | |
| 33 | Tomato___Leaf_Mold | | |
| 34 | Tomato___Septoria_leaf_spot | | |
| 35 | Tomato___Spider_mites | | |
| 36 | Tomato___Target_Spot | | |
| 37 | Tomato___Tomato_mosaic_virus | | |
| 38 | Tomato___Tomato_Yellow_Leaf_Curl_Virus | | |
| | **TOTAL** | | |

---

## Splits
| Split | File | Images | Notes |
|-------|------|--------|-------|
| Train | `data/splits/train.csv` | *(TBD)* | 70% per class, seed=42 |
| Validation | `data/splits/val.csv` | *(TBD)* | 15% per class, seed=42 |
| Test | `data/splits/test.csv` | *(TBD)* | 15% per class, seed=42 |
| Field Test | `data/splits/field_test.csv` | *(TBD)* | PlantDoc / real photos — never trained on |

---

## Cleaning Steps Performed
- [x] Exact duplicate removal (MD5 file hash)
- [x] Near-duplicate removal (pHash, hamming distance ≤ 10)
- [x] Converted all images to RGB JPEG (quality 95)
- [ ] Manual inspection of flagged classes (see `docs/data_issues.md`)

Removed duplicates log: `data/removed_duplicates.csv`

---

## ⚠️ Known Weaknesses
1. **Lab-controlled photos** — white/black backgrounds, not real farm conditions
2. **Near-duplicate leaves** — multiple shots of same leaf inflate test accuracy
3. **Missing Indian crops** — no rice, wheat, cotton, sugarcane (planned for Phase 10)
4. **Lab-to-field gap** — test accuracy on PlantVillage will be much higher than on real farm photos

---

## Review
| Reviewed By | Role | Date | Sign-off |
|-------------|------|------|---------|
| | Supervisor | | ☐ |
| | Data & AI Team | | ☐ |

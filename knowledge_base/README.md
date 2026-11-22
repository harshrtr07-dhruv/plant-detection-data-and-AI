# 🌿 Knowledge Base — Disease Cure Content
**Phase 6 | Plant Disease Detection System | VIT Bhopal University**

This folder contains one JSON file per disease class. Every file must be filled, reviewed by Dr. Jagriti Gupta (or an agronomist), and loaded into the database before Phase 8.

---

## 📁 Structure

```
knowledge_base/
├── README.md                         ← this file
├── schema.json                       ← field definitions & rules
├── _example_complete.json            ← fully filled reference entry
│
├── Apple___Apple_scab.json
├── Apple___Black_rot.json
├── Apple___Cedar_apple_rust.json
├── Apple___healthy.json
├── ...  (38 files total)
└── Tomato___Tomato_Yellow_Leaf_Curl_Virus.json
```

---

## ✅ Rules for Filling Entries

1. **Every field must be filled** — no empty strings, no `null` for required fields.
2. **Every treatment must have a source** — ICAR advisory, FAO, state agriculture dept, or peer-reviewed paper. Never fill from memory or AI alone.
3. **Chemical doses must come from cited sources** — add "follow product label and local agriculture officer's advice" to every chemical entry.
4. **`reviewed_by` and `reviewed_on` must be filled** before the entry goes to the database.
5. **Healthy classes** still need entries — with care tips, watering, fertiliser advice.

---

## 📚 Trusted Sources to Use

| Source | URL |
|--------|-----|
| ICAR (Indian Council of Agricultural Research) | https://icar.org.in |
| FAO Plant Production & Protection | https://www.fao.org/plant-production-protection |
| National Horticulture Board India | https://nhb.gov.in |
| eKRISHI (Ministry of Agriculture) | https://farmer.gov.in |
| UC Davis Plant Pathology | https://ipm.ucanr.edu |
| Plantix Disease Library | https://plantix.net |

---

## 🔄 Workflow

```
1. Open the JSON template for a disease
2. Fill all fields using trusted sources above
3. Record source + date next to each treatment
4. Submit to Dr. Jagriti Gupta for review
5. Fill reviewed_by and reviewed_on
6. Run the validator: python src/engine/kb_validator.py
7. Load into MongoDB (with backend team)
```

---

## 📊 Progress Tracker

| Class | Filled | Reviewed | Loaded |
|-------|--------|---------|--------|
| Apple___Apple_scab | ☐ | ☐ | ☐ |
| Apple___Black_rot | ☐ | ☐ | ☐ |
| Apple___Cedar_apple_rust | ☐ | ☐ | ☐ |
| Apple___healthy | ☐ | ☐ | ☐ |
| Blueberry___healthy | ☐ | ☐ | ☐ |
| Cherry___healthy | ☐ | ☐ | ☐ |
| Cherry___Powdery_mildew | ☐ | ☐ | ☐ |
| Corn___Cercospora_leaf_spot | ☐ | ☐ | ☐ |
| Corn___Common_rust | ☐ | ☐ | ☐ |
| Corn___healthy | ☐ | ☐ | ☐ |
| Corn___Northern_Leaf_Blight | ☐ | ☐ | ☐ |
| Grape___Black_rot | ☐ | ☐ | ☐ |
| Grape___Esca_(Black_Measles) | ☐ | ☐ | ☐ |
| Grape___healthy | ☐ | ☐ | ☐ |
| Grape___Leaf_blight | ☐ | ☐ | ☐ |
| Orange___Haunglongbing | ☐ | ☐ | ☐ |
| Peach___Bacterial_spot | ☐ | ☐ | ☐ |
| Peach___healthy | ☐ | ☐ | ☐ |
| Pepper___Bacterial_spot | ☐ | ☐ | ☐ |
| Pepper___healthy | ☐ | ☐ | ☐ |
| Potato___Early_blight | ☐ | ☐ | ☐ |
| Potato___healthy | ☐ | ☐ | ☐ |
| Potato___Late_blight | ☐ | ☐ | ☐ |
| Raspberry___healthy | ☐ | ☐ | ☐ |
| Soybean___healthy | ☐ | ☐ | ☐ |
| Squash___Powdery_mildew | ☐ | ☐ | ☐ |
| Strawberry___healthy | ☐ | ☐ | ☐ |
| Strawberry___Leaf_scorch | ☐ | ☐ | ☐ |
| Tomato___Bacterial_spot | ☐ | ☐ | ☐ |
| Tomato___Early_blight | ☐ | ☐ | ☐ |
| Tomato___healthy | ☐ | ☐ | ☐ |
| Tomato___Late_blight | ☐ | ☐ | ☐ |
| Tomato___Leaf_Mold | ☐ | ☐ | ☐ |
| Tomato___Septoria_leaf_spot | ☐ | ☐ | ☐ |
| Tomato___Spider_mites | ☐ | ☐ | ☐ |
| Tomato___Target_Spot | ☐ | ☐ | ☐ |
| Tomato___Tomato_mosaic_virus | ☐ | ☐ | ☐ |
| Tomato___Tomato_Yellow_Leaf_Curl_Virus | ☐ | ☐ | ☐ |

# 📄 API Contract — Plant Disease Detection Service
**Version:** 1.0 (Disease only — severity & cure_plan filled in Phase 7 & 8)  
**Last Updated:** 2026-11-23  
**Agreed Between:** Data & AI Team ↔ Node.js Backend Team

> [!IMPORTANT]
> The Node.js backend MUST call this service — NOT the React frontend directly.  
> Store the base URL in an environment variable: `MODEL_API_URL`  
> Allow **60+ seconds** for the first call after the service has been idle (Render sleep).

---

## Base URL
```
https://<your-render-service-name>.onrender.com
```
_(To be filled in after Phase 9 deployment)_

---

## Endpoints

### 1. `GET /health`
Health check — use this to wake the service before a demo.

**Response:**
```json
{
  "status": "ok",
  "model": "plant_model_v1.tflite",
  "timestamp": "2026-11-23T00:00:00Z"
}
```

---

### 2. `POST /predict`
Main prediction endpoint.

**Request** — `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file | ✅ | Leaf photo. JPEG or PNG. Max **5 MB**. |
| `crop` | string | ✅ | Crop name e.g. `"tomato"`, `"potato"`, `"pepper"` |
| `growth_stage` | string | ✅ | One of: `seedling`, `vegetative`, `flowering`, `fruiting` |

**Supported crop values:**
```
tomato, potato, pepper, apple, cherry, corn, grape,
peach, strawberry, squash
(rice, wheat, cotton, sugarcane — Phase 10)
```

---

**Response — Success `200 OK`**
```json
{
  "status": "ok",
  "prediction": {
    "disease": "Tomato Late Blight",
    "crop": "tomato",
    "confidence": 0.94,
    "top_3": [
      { "disease": "Tomato Late Blight", "confidence": 0.94 },
      { "disease": "Tomato Early Blight", "confidence": 0.04 },
      { "disease": "Tomato Healthy", "confidence": 0.02 }
    ]
  },
  "severity": {
    "level": "High",
    "lesion_area_percent": 38.2,
    "note": null
  },
  "cure_plan": {
    "symptoms": "Dark brown lesions with yellow halos on leaves...",
    "cause_type": "fungal",
    "spread_risk": "High — spreads rapidly in wet conditions",
    "organic_options": ["Remove infected leaves", "Neem oil spray"],
    "chemical_options": [
      {
        "product": "Mancozeb 75% WP",
        "dose": "2.5g per litre of water",
        "source": "ICAR advisory 2023"
      }
    ],
    "prevention": ["Avoid overhead watering", "Crop rotation"],
    "stage_advice": "At vegetative stage: focus on fungicide spray every 7 days",
    "reviewed_by": "Dr. Jagriti Gupta",
    "reviewed_on": "2026-11-23"
  },
  "warnings": [],
  "response_time_ms": 1240
}
```

> [!NOTE]
> **Version A (Phase 8 — disease only):** `severity` and `cure_plan` will be `null`.  
> **Version B (Phase 7+8 complete):** All fields filled.  
> The response shape stays the same — the website does NOT need to change.

---

**Response — Uncertain prediction `200 OK`**
```json
{
  "status": "uncertain",
  "message": "Confidence too low. Please retake the photo in good lighting.",
  "prediction": {
    "top_3": [
      { "disease": "Tomato Late Blight", "confidence": 0.52 },
      { "disease": "Tomato Early Blight", "confidence": 0.31 },
      { "disease": "Tomato Healthy", "confidence": 0.17 }
    ]
  },
  "severity": null,
  "cure_plan": null,
  "warnings": ["low_confidence"],
  "response_time_ms": 980
}
```

---

**Response — Wrong crop warning `200 OK`**
```json
{
  "status": "ok",
  "prediction": { "..." : "..." },
  "warnings": ["possible_wrong_crop — image looks like corn but potato was selected"],
  "severity": null,
  "cure_plan": null,
  "response_time_ms": 1100
}
```

---

**Error Responses**

| HTTP Code | `error_code` | Meaning |
|-----------|-------------|---------|
| `400` | `invalid_image` | File cannot be decoded as an image |
| `400` | `unsupported_format` | Only JPEG/PNG accepted |
| `400` | `file_too_large` | Image exceeds 5 MB |
| `400` | `missing_field` | `crop` or `growth_stage` not provided |
| `400` | `unsupported_crop` | Crop not in the supported list |
| `500` | `model_error` | Internal inference error |

```json
{
  "status": "error",
  "error_code": "file_too_large",
  "message": "Image must be under 5 MB.",
  "response_time_ms": 12
}
```

---

## Integration Notes for Node.js Backend

```javascript
// Example call from Node.js
const form = new FormData();
form.append('image', fs.createReadStream(imagePath));
form.append('crop', 'tomato');
form.append('growth_stage', 'vegetative');

const response = await axios.post(
  `${process.env.MODEL_API_URL}/predict`,
  form,
  {
    headers: form.getHeaders(),
    timeout: 90000  // 90 seconds — allow for Render cold start
  }
);
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-23 | Initial contract — disease + confidence only |
| 1.1 | _TBD_ | Add severity field (Phase 7) |
| 1.2 | _TBD_ | Add cure_plan field (Phase 8) |

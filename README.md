# Diabetes Prediction API

![CI](https://github.com/juanpjacobi/diabetes-ml-api/actions/workflows/ci.yml/badge.svg)

Production-ready REST API for multiclass diabetes prediction. A Random Forest classifier trained on clinical blood analysis data, served via FastAPI, deployed on Render, with an Angular frontend on Netlify.

**Live API:** `https://diabetes-ml-api-b2wo.onrender.com`
**Live Frontend:** [diabetes-ml-client.netlify.app](https://diabetes-ml-client.netlify.app)
**Frontend repo:** [diabetes-ml-frontend](https://github.com/juanpjacobi/diabetes-ml-frontend)

---

## Problem

Diabetes diagnosis requires interpreting multiple clinical markers simultaneously. This API takes 11 blood test values and returns a risk classification: no diabetes, prediabetes, or confirmed diabetes — enabling early intervention.

---

## Architecture

```
Angular 19 Frontend (Netlify)
         │
         │  POST /predict
         ▼
FastAPI Backend (Render)
         │
         ├── Pydantic validation (medical range checks)
         ├── sklearn Pipeline (RandomForest)
         └── Structured logging + request IDs
```

**Training flow:**

```
diabetes.csv → data_loader → train/test split → RandomForest Pipeline
    → evaluate (accuracy, classification report) → model.joblib + model_metadata.json
```

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| ML | scikit-learn (RandomForestClassifier) |
| Validation | Pydantic v2 |
| Serialization | joblib |
| Testing | pytest + httpx |
| Frontend | Angular 19 (standalone components, reactive forms) |
| Backend deploy | Render (auto-deploy on push) |
| Frontend deploy | Netlify (auto-deploy on push) |
| CI | GitHub Actions |

---

## Model

| Attribute | Value |
|---|---|
| Algorithm | RandomForestClassifier (100 estimators) |
| Accuracy | **95%** on held-out test set |
| Test split | 30%, stratified |
| Classes | 0 = No diabético, 1 = Predicción de diabetes, 2 = Diabético |
| Features | 11 clinical markers (see below) |

Training generates `artifacts/model_metadata.json` with version, accuracy, training timestamp, and expected features — enabling traceability across model updates.

---

## Project structure

```
diabetes-ml-api/
├── .github/
│   └── workflows/
│       └── ci.yml                    # Run tests on every push/PR to main
├── data/
│   └── diabetes.csv                  # 264 rows, 12 columns
├── artifacts/
│   ├── model.joblib                  # Serialized sklearn Pipeline
│   └── model_metadata.json           # Version, accuracy, trained_at, features
├── notebooks/
│   └── exploration.ipynb             # EDA, preprocessing, modeling experiments
├── training/
│   ├── config.py                     # Paths and constants
│   ├── data_loader.py                # CSV loading and X/y split
│   ├── train.py                      # Pipeline training + metadata generation
│   └── evaluate.py                   # Accuracy, classification report, confusion matrix
├── app/
│   ├── main.py                       # FastAPI app + request logging middleware
│   ├── core/config.py                # Model and metadata path settings
│   ├── schemas/prediction.py         # Pydantic models with medical range validation
│   ├── services/model_service.py     # Model loading, inference, structured logging
│   └── api/routes/prediction.py      # POST /predict endpoint
├── tests/
│   ├── conftest.py                   # Fixtures: TestClient, valid_payload
│   ├── test_health.py                # /health — status + model metadata fields
│   └── test_predict.py               # /predict — valid inputs and 6 invalid cases
├── requirements.txt
├── requirements-dev.txt              # pytest + httpx
└── render.yaml                       # Render deploy config
```

---

## Dataset

[Multiclass Diabetes Dataset](https://www.kaggle.com/datasets/yasserhessein/multiclass-diabetes-dataset) — Kaggle

| Feature | Type | Unit | Validation range |
|---|---|---|---|
| Gender | int | — | 0 (Female) or 1 (Male) |
| AGE | int | years | 1 – 120 |
| Urea | float | mg/dL | 0.5 – 200 |
| Cr | float | mg/dL | 0.1 – 50 |
| HbA1c | float | % | 2.0 – 20.0 |
| Chol | float | mmol/L | 1.0 – 20.0 |
| TG | float | mmol/L | 0.1 – 30.0 |
| HDL | float | mmol/L | 0.1 – 10.0 |
| LDL | float | mmol/L | 0.1 – 15.0 |
| VLDL | float | mmol/L | 0.1 – 10.0 |
| BMI | float | kg/m² | 10.0 – 80.0 |

Values outside these ranges return `422 Unprocessable Entity` with a descriptive error.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Train the model

```bash
python -m training.train
```

Outputs accuracy, classification report, confusion matrix, saves `artifacts/model.joblib` and `artifacts/model_metadata.json`.

---

## Run the API locally

```bash
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

---

## Run tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

10 tests covering:
- `/health` status and model metadata fields
- `/predict` valid input
- Missing required field → 422
- Invalid gender value → 422
- Negative / zero age → 422
- Out-of-range HbA1c, BMI, Cholesterol → 422

---

## Endpoints

### `GET /health`

Returns service status and model metadata.

```json
{
  "status": "ok",
  "model_version": "1.0.0",
  "accuracy": 0.95,
  "trained_at": "2026-03-24T15:30:00+00:00",
  "features": ["Gender", "AGE", "Urea", "Cr", "HbA1c", "Chol", "TG", "HDL", "LDL", "VLDL", "BMI"]
}
```

---

### `POST /predict`

**Request:**

```bash
curl -X POST https://diabetes-ml-api-b2wo.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": 1, "AGE": 50, "Urea": 4.7, "Cr": 46,
    "HbA1c": 4.9, "Chol": 4.2, "TG": 0.9,
    "HDL": 2.4, "LDL": 1.4, "VLDL": 0.5, "BMI": 24.0
  }'
```

**Response:**

```json
{
  "predicted_class": 0,
  "label": "No diabético"
}
```

**Validation error example** (HbA1c out of range):

```json
HTTP 422 Unprocessable Entity
{
  "detail": [{
    "loc": ["body", "HbA1c"],
    "msg": "Input should be less than or equal to 20",
    "type": "less_than_equal"
  }]
}
```

---

## Observability

Every request is assigned a unique `X-Request-ID` header (8-char UUID). The API logs method, path, status code, and duration in structured format:

```
{"time": "...", "level": "INFO", "message": "POST /predict", "request_id": "a1b2c3d4", "status_code": 200, "duration_ms": 42.1}
```

Model loading and prediction events are logged separately via `app.services.model_service`.

---

## Technical decisions

**Why RandomForest over simpler models?**
EDA in `notebooks/exploration.ipynb` showed non-linear feature interactions (e.g., HbA1c × BMI). RandomForest handles these without feature engineering, and 95% accuracy confirmed it was the right call for this dataset size (264 rows).

**Why multiclass instead of binary?**
The original dataset distinguishes prediabetes as a clinically meaningful intermediate state. Collapsing it to binary would discard actionable information.

**Why Pydantic validation with medical ranges?**
The model will return a prediction for any float input, including physiologically impossible values. Validating at the API boundary makes errors explicit and prevents silently misleading predictions.

**Why model_metadata.json alongside model.joblib?**
A serialized model is opaque. The metadata file makes the artifact self-describing: anyone (or any monitoring script) can read accuracy, training date, and expected features without loading the model.

---

## Possible next steps

- Save predictions to a database for monitoring input distributions over time
- `/metrics` endpoint exposing prediction counts per class
- Docker for environment parity between local and Render
- Explanation endpoint: given a prediction, return which features contributed most (SHAP values)

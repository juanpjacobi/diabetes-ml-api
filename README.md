# Diabetes Prediction API

REST API for multiclass diabetes prediction using a Random Forest model trained on clinical blood analysis data. Built with FastAPI and scikit-learn.

**Frontend:** [diabetes-ml-frontend](https://github.com/juanpjacobi/diabetes-ml-frontend)

---

## Overview

The model classifies patients into three categories based on 11 clinical features:

| Class | Label | Description |
|---|---|---|
| 0 | No diabético | No diabetes |
| 1 | Predicción de diabetes | Prediabetes / borderline |
| 2 | Diabético | Confirmed diabetes |

**Model performance:** 95% accuracy on held-out test set (30% split, stratified).

---

## Project structure

```
diabetes-ml-api/
├── data/
│   └── diabetes.csv              # 264 rows, 12 columns
├── artifacts/
│   └── model.joblib              # Serialized sklearn Pipeline
├── notebooks/
│   └── exploration.ipynb         # EDA, preprocessing, modeling experiments
├── training/
│   ├── config.py                 # Paths and constants
│   ├── data_loader.py            # CSV loading and X/y split
│   ├── train.py                  # Pipeline training and serialization
│   └── evaluate.py               # Accuracy, classification report, confusion matrix
├── app/
│   ├── main.py                   # FastAPI app
│   ├── core/config.py            # Model path settings
│   ├── schemas/prediction.py     # Pydantic request/response models
│   ├── services/model_service.py # Model loading and inference
│   └── api/routes/prediction.py  # POST /predict, GET /health endpoints
├── tests/
│   ├── conftest.py               # Fixtures: TestClient, valid_payload
│   ├── test_health.py            # GET /health
│   └── test_predict.py           # POST /predict — valid and invalid cases
├── requirements.txt
└── requirements-dev.txt          # pytest + httpx
```

---

## Dataset

[Multiclass Diabetes Dataset](https://www.kaggle.com/datasets/yasserhessein/multiclass-diabetes-dataset) — Kaggle

Features: `Gender`, `AGE`, `Urea`, `Cr`, `HbA1c`, `Chol`, `TG`, `HDL`, `LDL`, `VLDL`, `BMI`

---

## Setup

**Shared virtual environment** (from `dataScience/` root):

```bash
source .venv/bin/activate
```

Or create a dedicated one:

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

Outputs accuracy, classification report, confusion matrix, and saves `artifacts/model.joblib`.

---

## Run the API

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## Endpoints

### `GET /health`

Returns `200 OK` when the service is running.

```json
{ "status": "ok" }
```

---

### `POST /predict`

**Request body:**

```json
{
  "Gender": 1,
  "AGE": 50,
  "Urea": 4.7,
  "Cr": 46,
  "HbA1c": 4.9,
  "Chol": 4.2,
  "TG": 0.9,
  "HDL": 2.4,
  "LDL": 1.4,
  "VLDL": 0.5,
  "BMI": 24.0
}
```

| Field | Type | Unit | Notes |
|---|---|---|---|
| Gender | int | — | 0 = Female, 1 = Male |
| AGE | int | years | |
| Urea | float | mmol/L | |
| Cr | float | µmol/L | Creatinine |
| HbA1c | float | % | Key diabetes indicator |
| Chol | float | mmol/L | Total cholesterol |
| TG | float | mmol/L | Triglycerides |
| HDL | float | mmol/L | |
| LDL | float | mmol/L | |
| VLDL | float | mmol/L | |
| BMI | float | kg/m² | |

**Response:**

```json
{
  "predicted_class": 0,
  "label": "No diabético"
}
```
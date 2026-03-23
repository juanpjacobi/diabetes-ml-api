import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from app.core.config import MODEL_PATH
from app.schemas.prediction import CLASS_LABELS, PredictionRequest, PredictionResponse

_model: Pipeline | None = None

FEATURE_ORDER = [
    "Gender", "AGE", "Urea", "Cr", "HbA1c",
    "Chol", "TG", "HDL", "LDL", "VLDL", "BMI",
]


def load_model() -> Pipeline:
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(request: PredictionRequest) -> PredictionResponse:
    model = load_model()
    data = pd.DataFrame([request.model_dump()])[FEATURE_ORDER]
    predicted_class = int(model.predict(data)[0])
    return PredictionResponse(
        predicted_class=predicted_class,
        label=CLASS_LABELS[predicted_class],
    )

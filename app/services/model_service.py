import logging
import time

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from app.core.config import MODEL_PATH
from app.schemas.prediction import CLASS_LABELS, PredictionRequest, PredictionResponse

logger = logging.getLogger(__name__)

_model: Pipeline | None = None

FEATURE_ORDER = [
    "Gender", "AGE", "Urea", "Cr", "HbA1c",
    "Chol", "TG", "HDL", "LDL", "VLDL", "BMI",
]


def load_model() -> Pipeline:
    global _model
    if _model is None:
        logger.info("Loading model from disk", extra={"path": str(MODEL_PATH)})
        _model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully")
    return _model


def predict(request: PredictionRequest) -> PredictionResponse:
    model = load_model()
    data = pd.DataFrame([request.model_dump()])[FEATURE_ORDER]

    start = time.perf_counter()
    predicted_class = int(model.predict(data)[0])
    duration_ms = round((time.perf_counter() - start) * 1000, 2)

    logger.info(
        "Prediction made",
        extra={
            "predicted_class": predicted_class,
            "label": CLASS_LABELS[predicted_class],
            "duration_ms": duration_ms,
        },
    )

    return PredictionResponse(
        predicted_class=predicted_class,
        label=CLASS_LABELS[predicted_class],
    )

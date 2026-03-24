import json
from datetime import datetime, timezone

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from training.config import ARTIFACTS_DIR, MODEL_PATH, RANDOM_STATE, TEST_SIZE
from training.data_loader import load_dataset
from training.evaluate import evaluate

METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"

FEATURE_ORDER = [
    "Gender", "AGE", "Urea", "Cr", "HbA1c",
    "Chol", "TG", "HDL", "LDL", "VLDL", "BMI",
]

CLASS_LABELS = {"0": "No diabético", "1": "Predicción de diabetes", "2": "Diabético"}


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            random_state=RANDOM_STATE,
        )),
    ])


def train() -> None:
    X, y = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    metrics = evaluate(pipeline, X_test, y_test)

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

    metadata = {
        "model_version": "1.0.0",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "accuracy": metrics["accuracy"],
        "features": FEATURE_ORDER,
        "n_classes": 3,
        "class_labels": CLASS_LABELS,
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    print(f"Metadata saved to {METADATA_PATH}")


if __name__ == "__main__":
    train()

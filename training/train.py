import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from training.config import ARTIFACTS_DIR, MODEL_PATH, RANDOM_STATE, TEST_SIZE
from training.data_loader import load_dataset
from training.evaluate import evaluate


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

    evaluate(pipeline, X_test, y_test)

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()

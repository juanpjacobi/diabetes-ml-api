from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "diabetes.csv"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "model.joblib"

TARGET_COLUMN = "Class"
TEST_SIZE = 0.3
RANDOM_STATE = 42

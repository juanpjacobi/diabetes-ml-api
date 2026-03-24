from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "artifacts" / "model.joblib"
METADATA_PATH = BASE_DIR / "artifacts" / "model_metadata.json"

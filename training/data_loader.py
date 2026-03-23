import pandas as pd
from pathlib import Path
from training.config import DATA_PATH, TARGET_COLUMN


def load_dataset(path: Path = DATA_PATH) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)
    df = df.drop_duplicates()

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    return X, y

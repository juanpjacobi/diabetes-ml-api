import sqlite3
from datetime import datetime, timezone

from app.core.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT    NOT NULL,
                gender          INTEGER,
                age             INTEGER,
                urea            REAL,
                cr              REAL,
                hba1c           REAL,
                chol            REAL,
                tg              REAL,
                hdl             REAL,
                ldl             REAL,
                vldl            REAL,
                bmi             REAL,
                predicted_class INTEGER NOT NULL,
                duration_ms     REAL
            )
        """)


def save_prediction(inputs: dict, predicted_class: int, duration_ms: float) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO predictions
                (timestamp, gender, age, urea, cr, hba1c, chol, tg, hdl, ldl, vldl, bmi,
                 predicted_class, duration_ms)
            VALUES
                (:timestamp, :gender, :age, :urea, :cr, :hba1c, :chol, :tg, :hdl, :ldl, :vldl, :bmi,
                 :predicted_class, :duration_ms)
            """,
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "gender": inputs.get("Gender"),
                "age": inputs.get("AGE"),
                "urea": inputs.get("Urea"),
                "cr": inputs.get("Cr"),
                "hba1c": inputs.get("HbA1c"),
                "chol": inputs.get("Chol"),
                "tg": inputs.get("TG"),
                "hdl": inputs.get("HDL"),
                "ldl": inputs.get("LDL"),
                "vldl": inputs.get("VLDL"),
                "bmi": inputs.get("BMI"),
                "predicted_class": predicted_class,
                "duration_ms": duration_ms,
            },
        )


def get_metrics() -> dict:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]

        rows = conn.execute(
            "SELECT predicted_class, COUNT(*) as count FROM predictions GROUP BY predicted_class"
        ).fetchall()

        avg_duration = conn.execute(
            "SELECT AVG(duration_ms) FROM predictions"
        ).fetchone()[0]

    by_class = {str(row["predicted_class"]): row["count"] for row in rows}

    return {
        "total_predictions": total,
        "by_class": by_class,
        "avg_duration_ms": round(avg_duration, 2) if avg_duration else 0.0,
    }
import pytest
from fastapi.testclient import TestClient

import app.db.database as db_module
from app.main import app


@pytest.fixture(autouse=True)
def use_in_memory_db(monkeypatch, tmp_path):
    import sqlite3

    test_db = tmp_path / "test.db"

    def make_connection():
        conn = sqlite3.connect(str(test_db))
        conn.row_factory = sqlite3.Row
        return conn

    monkeypatch.setattr(db_module, "get_connection", make_connection)
    db_module.init_db()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_payload():
    return {
        "Gender": 1,
        "AGE": 50,
        "Urea": 4.7,
        "Cr": 46.0,
        "HbA1c": 4.9,
        "Chol": 4.2,
        "TG": 0.9,
        "HDL": 2.4,
        "LDL": 1.4,
        "VLDL": 0.5,
        "BMI": 24.0,
    }

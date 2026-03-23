import pytest
from fastapi.testclient import TestClient

from app.main import app


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

from app.schemas.prediction import CLASS_LABELS


def test_predict_valid(client, valid_payload):
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "label" in data
    assert data["predicted_class"] in CLASS_LABELS
    assert data["label"] == CLASS_LABELS[data["predicted_class"]]


def test_predict_missing_field(client, valid_payload):
    del valid_payload["HbA1c"]
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_invalid_gender(client, valid_payload):
    valid_payload["Gender"] = 5
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_negative_age(client, valid_payload):
    valid_payload["AGE"] = -1
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_zero_age(client, valid_payload):
    valid_payload["AGE"] = 0
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_invalid_hba1c(client, valid_payload):
    valid_payload["HbA1c"] = -1.0
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_invalid_bmi(client, valid_payload):
    valid_payload["BMI"] = 0.0
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422


def test_predict_invalid_chol(client, valid_payload):
    valid_payload["Chol"] = 999.0
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 422

def test_metrics_returns_ok(client):
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_structure(client):
    response = client.get("/metrics")
    data = response.json()
    assert "total_predictions" in data
    assert "by_class" in data
    assert "avg_duration_ms" in data


def test_metrics_count_increases_after_prediction(client, valid_payload):
    before = client.get("/metrics").json()["total_predictions"]
    client.post("/predict", json=valid_payload)
    after = client.get("/metrics").json()["total_predictions"]
    assert after == before + 1


def test_metrics_by_class_has_labels(client, valid_payload):
    client.post("/predict", json=valid_payload)
    data = client.get("/metrics").json()
    for entry in data["by_class"].values():
        assert "label" in entry
        assert "count" in entry
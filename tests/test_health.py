def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_health_includes_model_metadata(client):
    response = client.get("/health")
    data = response.json()
    assert "model_version" in data
    assert "accuracy" in data
    assert "trained_at" in data
    assert "features" in data
    assert isinstance(data["features"], list)
    assert len(data["features"]) == 11

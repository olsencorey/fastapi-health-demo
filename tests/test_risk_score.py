from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_low_risk():
    payload = {"age": 25, "smoker": False, "bmi": 22.0}
    response = client.post("/risk-score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_band"] in ["low", "medium", "high"]

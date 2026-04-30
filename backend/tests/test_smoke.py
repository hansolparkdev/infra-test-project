from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    """GET /api/health returns OK JSON (CI smoke test against FastAPI app)."""
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "env" in payload

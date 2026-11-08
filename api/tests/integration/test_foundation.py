from fastapi.testclient import TestClient

from app.main import app


def test_live_and_ready():
    with TestClient(app) as client:
        assert client.get("/health/live").status_code == 200
        assert client.get("/health/ready").status_code == 200


def test_anonymous_catalog_is_denied():
    with TestClient(app) as client:
        assert client.get("/api/v1/locations").status_code == 401

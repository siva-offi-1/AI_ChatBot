from fastapi.testclient import TestClient
from app.main import app

def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

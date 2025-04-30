from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {
        "app_name": "Mini Rag App",
        "app_version": "0.1",
    }
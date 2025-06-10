from fastapi.testclient import TestClient
from src.main import app

tc = TestClient(app)

def test_alive():
    response = tc.get("/health/alive")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

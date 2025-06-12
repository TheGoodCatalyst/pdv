from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_generate_proof():
    resp = client.post("/proof/", json={"data": "hello"})
    assert resp.status_code == 200
    assert "proof" in resp.json()

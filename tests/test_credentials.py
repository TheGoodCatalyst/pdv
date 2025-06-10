import os
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.storage.database import Base, engine

client = TestClient(app)


TEST_DB = "sqlite:///./test_api.db"


@pytest.fixture(autouse=True)
def setup_db():
    os.environ["DATABASE_URL"] = TEST_DB
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_api.db"):
        os.remove("test_api.db")


def test_create_and_get_credential():
    payload = {"user_id": "u1", "cred_type": "Test", "blob": "secret"}
    resp = client.post("/credentials/", json=payload)
    assert resp.status_code == 200
    assert resp.json()["blob"] == "secret"

    resp_get = client.get("/credentials/u1/Test")
    assert resp_get.status_code == 200
    assert resp_get.json()["blob"] == "secret"


def test_revoke_credential():
    payload = {"user_id": "u2", "cred_type": "Test", "blob": "data"}
    client.post("/credentials/", json=payload)
    resp = client.post("/credentials/u2/Test/revoke")
    assert resp.status_code == 200

    resp_get = client.get("/credentials/u2/Test")
    assert resp_get.status_code == 200
    assert resp_get.json()["status"] == "revoked"

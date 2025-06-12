import os
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.storage.database import Base, engine

client = TestClient(app)
TEST_DB = "sqlite:///./test_consents.db"

@pytest.fixture(autouse=True)
def setup_db():
    os.environ["DATABASE_URL"] = TEST_DB
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_consents.db"):
        os.remove("test_consents.db")


def test_record_and_list_consent():
    payload = {"user_id": "u1", "service": "svc", "scope": "email", "decision": "granted"}
    resp = client.post("/consents/", json=payload)
    assert resp.status_code == 200
    consent_id = resp.json()["id"]

    resp_list = client.get("/consents/u1?service=svc")
    assert resp_list.status_code == 200
    data = resp_list.json()
    assert len(data) == 1
    assert data[0]["id"] == consent_id

import os
import pytest
from sqlalchemy import inspect
from src.storage.database import engine, Base, SessionLocal
from src.storage.models import UserProfile, Credential, CredentialStatus


# Ensure fresh SQLite file per test run
TEST_DB = "sqlite:///./test_pdv.db"


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # override URL
    os.environ['DATABASE_URL'] = TEST_DB
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_pdv.db"):
        os.remove("test_pdv.db")


def test_tables_created():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "user_profiles" in tables
    assert "credentials" in tables


def test_insert_credential():
    db = SessionLocal()
    profile = UserProfile(
        user_id="user1", name="Alice", email="alice@example.com"
    )
    db.add(profile)
    cred = Credential(
        user_id="user1", cred_type="Test", blob=b"encrypteddata"
    )
    db.add(cred)
    db.commit()
    retrieved = db.query(Credential).filter_by(user_id="user1").one()
    assert retrieved.status == CredentialStatus.active
    db.close()

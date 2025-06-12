from sqlalchemy import Column, String, DateTime, Enum, JSON
from sqlalchemy.dialects.sqlite import BLOB
from datetime import datetime
from src.storage.database import Base
import enum


class CredentialStatus(enum.Enum):
    active = "active"
    revoked = "revoked"
    expired = "expired"


class UserProfile(Base):
    __tablename__ = "user_profiles"
    user_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    dob = Column(DateTime)
    preferences = Column(JSON)


class Credential(Base):
    __tablename__ = "credentials"
    user_id = Column(String, primary_key=True)
    cred_type = Column(String, primary_key=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    status = Column(Enum(CredentialStatus), default=CredentialStatus.active)
    metadata_ = Column("metadata", JSON)
    blob = Column(BLOB, nullable=False)  # encrypted credential payload


class ConsentDecision(enum.Enum):
    granted = "granted"
    denied = "denied"


class Consent(Base):
    __tablename__ = "consents"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    service = Column(String, index=True)
    scope = Column(String)
    decision = Column(Enum(ConsentDecision))
    timestamp = Column(DateTime, default=datetime.utcnow)

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from src.storage.database import get_db
from src.storage.models import Consent, ConsentDecision

router = APIRouter()

class ConsentIn(BaseModel):
    user_id: str
    service: str
    scope: str
    decision: ConsentDecision

class ConsentOut(BaseModel):
    id: str
    user_id: str
    service: str
    scope: str
    decision: ConsentDecision

@router.post("/", response_model=ConsentOut, tags=["Consents"])
async def record_consent(data: ConsentIn, db: Session = Depends(get_db)):
    consent = Consent(
        id=str(uuid.uuid4()),
        user_id=data.user_id,
        service=data.service,
        scope=data.scope,
        decision=data.decision,
    )
    db.add(consent)
    db.commit()
    db.refresh(consent)
    return consent

@router.get("/{user_id}", response_model=list[ConsentOut], tags=["Consents"])
async def list_consents(user_id: str, service: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Consent).filter_by(user_id=user_id)
    if service:
        query = query.filter_by(service=service)
    return query.all()

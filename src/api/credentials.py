from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.storage.database import get_db
from src.storage.models import Credential, CredentialStatus
from src.kms.local_kms import LocalKMS

router = APIRouter()

# simple in-memory KMS instance for demo purposes
kms = LocalKMS()
kms.generate_key("default")


class CredentialIn(BaseModel):
    user_id: str
    cred_type: str
    blob: str


class CredentialOut(BaseModel):
    user_id: str
    cred_type: str
    status: CredentialStatus
    blob: str


@router.post("/", response_model=CredentialOut, tags=["Credentials"])
async def create_credential(data: CredentialIn, db: Session = Depends(get_db)):
    ciphertext = kms.encrypt("default", data.blob.encode())
    cred = Credential(
        user_id=data.user_id,
        cred_type=data.cred_type,
        blob=ciphertext,
    )
    db.add(cred)
    db.commit()
    db.refresh(cred)
    plaintext = kms.decrypt("default", cred.blob).decode()
    return CredentialOut(
        user_id=cred.user_id,
        cred_type=cred.cred_type,
        status=cred.status,
        blob=plaintext,
    )


@router.get("/{user_id}/{cred_type}",
            response_model=CredentialOut,
            tags=["Credentials"])
async def get_credential(
    user_id: str, cred_type: str, db: Session = Depends(get_db)
):
    cred = db.query(Credential).filter_by(
        user_id=user_id, cred_type=cred_type
    ).first()
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found")
    plaintext = kms.decrypt("default", cred.blob).decode()
    return CredentialOut(
        user_id=cred.user_id,
        cred_type=cred.cred_type,
        status=cred.status,
        blob=plaintext,
    )


@router.post("/{user_id}/{cred_type}/revoke", tags=["Credentials"])
async def revoke_credential(
    user_id: str, cred_type: str, db: Session = Depends(get_db)
):
    cred = db.query(Credential).filter_by(
        user_id=user_id, cred_type=cred_type
    ).first()
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found")
    cred.status = CredentialStatus.revoked
    db.commit()
    return {"status": "revoked"}

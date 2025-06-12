from mcp.server.fastmcp import FastMCP
import uuid
from src.storage.database import SessionLocal
from src.storage.models import (
    Credential,
    CredentialStatus,
    Consent,
    ConsentDecision,
)
from src.kms.registry import kms

mcp = FastMCP("PDV MCP", stateless_http=True)


@mcp.tool(description="Create a new credential")
def create_credential(user_id: str, cred_type: str, blob: str) -> dict:
    with SessionLocal() as db:
        ciphertext = kms.encrypt("default", blob.encode())
        cred = Credential(user_id=user_id, cred_type=cred_type, blob=ciphertext)
        db.add(cred)
        db.commit()
        db.refresh(cred)
        plaintext = kms.decrypt("default", cred.blob).decode()
        return {
            "user_id": cred.user_id,
            "cred_type": cred.cred_type,
            "status": cred.status.value,
            "blob": plaintext,
        }

@mcp.tool(description="Retrieve a credential")
def get_credential(user_id: str, cred_type: str) -> dict:
    with SessionLocal() as db:
        cred = db.query(Credential).filter_by(user_id=user_id, cred_type=cred_type).first()
        if not cred:
            raise ValueError("Credential not found")
        plaintext = kms.decrypt("default", cred.blob).decode()
        return {
            "user_id": cred.user_id,
            "cred_type": cred.cred_type,
            "status": cred.status.value,
            "blob": plaintext,
        }

@mcp.tool(description="Revoke a credential")
def revoke_credential(user_id: str, cred_type: str) -> dict:
    with SessionLocal() as db:
        cred = db.query(Credential).filter_by(user_id=user_id, cred_type=cred_type).first()
        if not cred:
            raise ValueError("Credential not found")
        cred.status = CredentialStatus.revoked
        db.commit()
        return {"status": "revoked"}


@mcp.tool(description="Record a user consent decision")
def record_consent(user_id: str, service: str, scope: str, decision: str) -> dict:
    with SessionLocal() as db:
        consent = Consent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            service=service,
            scope=scope,
            decision=ConsentDecision(decision),
        )
        db.add(consent)
        db.commit()
        db.refresh(consent)
        return {
            "id": consent.id,
            "user_id": consent.user_id,
            "service": consent.service,
            "scope": consent.scope,
            "decision": consent.decision.value,
        }


@mcp.tool(description="Check the latest consent decision for a scope")
def check_consent(user_id: str, service: str, scope: str) -> dict:
    with SessionLocal() as db:
        consent = (
            db.query(Consent)
            .filter_by(user_id=user_id, service=service, scope=scope)
            .order_by(Consent.timestamp.desc())
            .first()
        )
        if not consent:
            return {"decision": "none"}
        return {"decision": consent.decision.value}


@mcp.tool(description="Generate a signed proof of data")
def generate_proof(data: str) -> dict:
    signer = kms.get_signer("default")
    signature = signer(data.encode()).hex()
    return {"proof": signature}

@mcp.resource("pdv://health")
def health() -> str:
    return "healthy"

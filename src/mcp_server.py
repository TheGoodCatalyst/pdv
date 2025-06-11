from mcp.server.fastmcp import FastMCP
from src.storage.database import SessionLocal
from src.storage.models import Credential, CredentialStatus
from src.kms.local_kms import LocalKMS

mcp = FastMCP("PDV MCP", stateless_http=True)

_kms = LocalKMS()
_kms.generate_key("default")

@mcp.tool(description="Create a new credential")
def create_credential(user_id: str, cred_type: str, blob: str) -> dict:
    with SessionLocal() as db:
        ciphertext = _kms.encrypt("default", blob.encode())
        cred = Credential(user_id=user_id, cred_type=cred_type, blob=ciphertext)
        db.add(cred)
        db.commit()
        db.refresh(cred)
        plaintext = _kms.decrypt("default", cred.blob).decode()
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
        plaintext = _kms.decrypt("default", cred.blob).decode()
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

@mcp.resource("pdv://health")
def health() -> str:
    return "healthy"

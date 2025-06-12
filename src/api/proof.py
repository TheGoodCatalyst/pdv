from fastapi import APIRouter
from pydantic import BaseModel
from src.kms.registry import kms

router = APIRouter()

class ProofRequest(BaseModel):
    data: str

class ProofResponse(BaseModel):
    proof: str

@router.post("/", response_model=ProofResponse, tags=["Proofs"])
async def generate_proof(req: ProofRequest):
    signer = kms.get_signer("default")
    sig = signer(req.data.encode()).hex()
    return ProofResponse(proof=sig)

from fastapi import FastAPI
from src.api.health import router as health_router
from src.api.credentials import router as credentials_router
from src.api.consents import router as consents_router
from src.api.proof import router as proof_router
from src.mcp_server import mcp

app = FastAPI(title="Personal Data Vault Service")
app.include_router(health_router, prefix="/health")
app.include_router(credentials_router, prefix="/credentials")
app.include_router(consents_router, prefix="/consents")
app.include_router(proof_router, prefix="/proof")
app.mount("/mcp", mcp.streamable_http_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

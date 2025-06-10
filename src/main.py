from fastapi import FastAPI
from src.api.health import router as health_router

app = FastAPI(title="Personal Data Vault Service")
app.include_router(health_router, prefix="/health")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

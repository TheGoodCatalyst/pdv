from fastapi import APIRouter


router = APIRouter()


@router.get("/alive", tags=["Health"])
async def alive():
    return {"status": "healthy"}

from fastapi import APIRouter
router = APIRouter(tags=["Health"])

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "The local llm api server is up and running",
    }
@router.get("/ready")
async def ready():
    return {
        "status": "ready",
        "message": "The local llm api server is ready to take requests",
    }
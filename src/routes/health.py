from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health", tags=["API Health check"])
async def health():
    return {"status": "AI Assistant is running"}

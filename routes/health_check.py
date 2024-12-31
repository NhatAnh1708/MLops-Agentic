from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get("/health", tags=["Check AI Services"])
def health_check():
    """API check health of service"""
    headers = {"X-Custom-Header": "API GET health check"}
    return HTTPException(status_code=200, detail="Service is running", headers=headers)

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.api.responses import success_response
from app.schemas.base import APIResponse

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    database: str
    cache: str

@router.get("/", response_model=APIResponse[HealthResponse], status_code=status.HTTP_200_OK)
async def health_check():
    """
    Basic health check endpoint for Kubernetes liveness/readiness probes.
    """
    data = HealthResponse(
        status="healthy",
        database="disconnected", # Placeholder
        cache="disconnected"     # Placeholder
    )
    return success_response(data)

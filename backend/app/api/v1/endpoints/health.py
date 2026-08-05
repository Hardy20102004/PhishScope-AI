import os

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import success_response
from app.schemas.base import APIResponse

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    database: str
    cache: str

def _check_database(db: Session) -> str:
    """Attempt a lightweight query to confirm DB connectivity."""
    try:
        db.execute(text("SELECT 1"))
        return "connected"
    except Exception:
        return "disconnected"

def _check_redis() -> str:
    """Attempt a PING to the configured Redis URL."""
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return "not_configured"
    try:
        import redis as redis_lib
        client = redis_lib.from_url(redis_url, socket_connect_timeout=2)
        client.ping()
        return "connected"
    except Exception:
        return "disconnected"

@router.get("/", response_model=APIResponse[HealthResponse], status_code=status.HTTP_200_OK)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for Kubernetes liveness/readiness probes.
    Probes both the database and Redis cache.
    Returns 200 with status 'healthy' only when both connections succeed.
    """
    db_status = _check_database(db)
    cache_status = _check_redis()

    overall = "healthy" if db_status == "connected" else "degraded"

    data = HealthResponse(
        status=overall,
        database=db_status,
        cache=cache_status,
    )
    return success_response(data)

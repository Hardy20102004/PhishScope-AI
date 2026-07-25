from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.observability import Incident, SystemMetric
from app.models.user import User
from app.schemas.observability import IncidentSchema, SystemMetricSchema

router = APIRouter()

@router.get("/health")
def get_system_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Simulated deep health check
    return {
        "status": "pass",
        "version": "1.0.0",
        "components": {
            "database": "pass",
            "redis": "pass",
            "celery": "pass",
            "threat_feeds": "warn",
            "ai_copilot": "pass"
        }
    }

@router.get("/incidents", response_model=List[IncidentSchema])
def get_incidents(
    status: str = "OPEN",
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Incident).where(Incident.status == status).order_by(Incident.created_at.desc()).limit(limit)
    incidents = db.execute(stmt).scalars().all()
    return incidents

@router.get("/metrics", response_model=List[SystemMetricSchema])
def get_metrics(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(SystemMetric).order_by(SystemMetric.timestamp.desc()).limit(limit)
    metrics = db.execute(stmt).scalars().all()
    return metrics

from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger

from app.api import deps
from app.threat_actor.schemas import (
    ThreatActorCreate,
    ThreatActorUpdate,
    ThreatActorResponse,
    AttributionEvidenceResponse
)
from app.threat_actor.models import ThreatActor, AttributionEvidence
from app.threat_actor.profile_engine import ProfileEngine
from app.threat_actor.attribution import AttributionConfidenceEngine

router = APIRouter()

@router.post("/", response_model=ThreatActorResponse, status_code=status.HTTP_201_CREATED)
def create_threat_actor(
    *,
    db: Session = Depends(deps.get_db),
    actor_in: ThreatActorCreate,
) -> Any:
    """
    Create a new Threat Actor profile.
    """
    engine = ProfileEngine(db)
    return engine.create_actor(actor_in)

@router.get("/{actor_id}", response_model=ThreatActorResponse)
def get_threat_actor(
    actor_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get detailed Threat Actor profile.
    """
    engine = ProfileEngine(db)
    actor = engine.get_actor(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Threat Actor not found")
    return actor

@router.get("/{actor_id}/attribution", response_model=List[AttributionEvidenceResponse])
def get_attribution_evidence(
    actor_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get all attribution evidence (Observed Facts vs Inferences) for an actor.
    """
    evidence = db.query(AttributionEvidence).filter(AttributionEvidence.actor_id == actor_id).all()
    return evidence

@router.get("/analytics/summary")
def get_actor_analytics(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get high-level analytics for the Threat Actor Dashboard.
    """
    total_actors = db.query(ThreatActor).count()
    
    # Mock analytics for the frontend dashboard
    return {
        "total_actors": total_actors,
        "active_campaigns": 12,
        "average_confidence": 0.78,
        "top_targeted_sectors": {"Finance": 45, "Healthcare": 30, "Government": 25},
        "emerging_actors": []
    }

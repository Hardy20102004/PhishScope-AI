from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.reputation_engine.schemas import (
    ProfileBase,
    ProfileResponse,
    HistoryResponse,
    EvidenceCreate,
    EvidenceResponse
)
from app.reputation_engine.models import ReputationProfile, ReputationEvidence, ReputationTrend
from app.reputation_engine.scoring import ReputationScoringEngine
from app.reputation_engine.evidence import EvidenceWeightingEngine
from app.reputation_engine.trends import TrendAnalysisEngine
from app.reputation_engine.relationships import RelationshipInfluenceEngine

router = APIRouter()

@router.get("/{entity_id}", response_model=ProfileResponse)
def get_reputation_profile(
    entity_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get the current reputation profile for an entity.
    If it doesn't exist, initializes a neutral profile.
    """
    profile = db.query(ReputationProfile).filter(ReputationProfile.entity_id == entity_id).first()
    if not profile:
        profile = ReputationProfile(
            entity_id=entity_id,
            entity_type="Unknown",
            risk_score=0.0,
            trust_score=50.0,
            trend=ReputationTrend.NEW
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.post("/{entity_id}/score", response_model=ProfileResponse)
def submit_evidence(
    entity_id: str,
    evidence_in: EvidenceCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Submit new evidence to recalculate the entity's score.
    """
    profile = get_reputation_profile(entity_id, db)
    
    # Weigh evidence
    evidence_engine = EvidenceWeightingEngine(db)
    adj_risk, adj_trust = evidence_engine.weigh_evidence(
        source=evidence_in.source, 
        base_risk_delta=evidence_in.risk_delta, 
        base_trust_delta=evidence_in.trust_delta
    )
    
    # Store evidence
    evidence = ReputationEvidence(
        profile_id=profile.id,
        source=evidence_in.source,
        description=evidence_in.description,
        risk_delta=adj_risk,
        trust_delta=adj_trust,
        weight=evidence_in.weight
    )
    db.add(evidence)
    
    # Apply to score
    scoring = ReputationScoringEngine(db)
    profile = scoring.apply_evidence(profile, adj_risk, adj_trust, trigger_event=evidence_in.source)
    
    # Update trends
    trends = TrendAnalysisEngine(db)
    trends.evaluate_trend(profile)
    
    return profile

@router.get("/{entity_id}/history", response_model=List[HistoryResponse])
def get_reputation_history(
    entity_id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Fetch the timeline of score changes.
    """
    profile = get_reputation_profile(entity_id, db)
    return profile.history

@router.get("/analytics/summary")
def get_reputation_analytics(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get high-level reputation analytics for the dashboard.
    """
    total = db.query(ReputationProfile).count()
    high_risk = db.query(ReputationProfile).filter(ReputationProfile.risk_score >= 80).count()
    declining = db.query(ReputationProfile).filter(ReputationProfile.trend == ReputationTrend.DECLINING).count()
    
    return {
        "total_profiles_tracked": total,
        "high_risk_entities": high_risk,
        "declining_reputations": declining,
        "average_system_trust": 65.4 # Mock metric
    }

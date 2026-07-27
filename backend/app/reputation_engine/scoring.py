from sqlalchemy.orm import Session
from app.reputation_engine.models import ReputationProfile, ReputationHistory
from loguru import logger
import uuid
from datetime import datetime, timezone

class ReputationScoringEngine:
    """
    Calculates dynamic Risk and Trust scores for entities.
    """
    def __init__(self, db: Session):
        self.db = db

    def apply_evidence(self, profile: ReputationProfile, risk_delta: float, trust_delta: float, trigger_event: str) -> ReputationProfile:
        """
        Applies deltas to the current profile and logs the history.
        Ensures scores remain bounded between 0.0 and 100.0.
        """
        logger.info(f"Applying evidence to profile {profile.entity_id}: Risk {risk_delta:+.2f}, Trust {trust_delta:+.2f}")
        
        # Apply deltas and bound between 0 and 100
        new_risk = max(0.0, min(100.0, profile.risk_score + risk_delta))
        new_trust = max(0.0, min(100.0, profile.trust_score + trust_delta))
        
        profile.risk_score = new_risk
        profile.trust_score = new_trust
        
        # Log history
        history = ReputationHistory(
            profile_id=profile.id,
            risk_score=new_risk,
            trust_score=new_trust,
            trigger_event=trigger_event
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(profile)
        
        return profile

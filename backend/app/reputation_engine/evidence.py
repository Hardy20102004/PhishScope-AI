from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.reputation_engine.models import ReputationEvidence
import uuid

class EvidenceWeightingEngine:
    """
    Evaluates evidence reliability and age decay.
    """
    def __init__(self, db: Session):
        self.db = db
        
        # Reliability matrix mock
        self.source_reliability = {
            "Threat Actor Intelligence": 1.5,
            "IOC Correlation Engine": 1.2,
            "Analyst Validation": 2.0,
            "External Feed (Low Confidence)": 0.5
        }

    def weigh_evidence(self, source: str, base_risk_delta: float, base_trust_delta: float) -> tuple[float, float]:
        """
        Adjusts deltas based on source reliability.
        In a real system, time decay (e.g. half-life equations for older evidence) is also calculated here.
        """
        weight = self.source_reliability.get(source, 1.0)
        
        return base_risk_delta * weight, base_trust_delta * weight

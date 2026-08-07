from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.threat_actor.models import AttributionEvidence, ThreatActor
import uuid

class AttributionConfidenceEngine:
    """
    Calculates confidence scores based on deterministic facts and AI inferences.
    """
    def __init__(self, db: Session):
        self.db = db

    def calculate_actor_confidence(self, actor_id: uuid.UUID) -> float:
        """
        Re-evaluates the overall confidence score of a Threat Actor profile based on its evidence.
        """
        evidence_list = self.db.query(AttributionEvidence).filter(AttributionEvidence.actor_id == actor_id).all()
        if not evidence_list:
            return 0.0

        # Facts carry more weight than inferences
        fact_weight = 1.0
        inference_weight = 0.5
        
        total_score = 0.0
        max_possible = 0.0
        
        for ev in evidence_list:
            weight = fact_weight if ev.is_observed_fact else inference_weight
            total_score += (ev.confidence * weight)
            max_possible += weight

        if max_possible == 0:
            return 0.0
            
        return total_score / max_possible

    def add_evidence(self, actor_id: uuid.UUID, description: str, is_fact: bool, confidence: float, ref_id: uuid.UUID = None, ref_type: str = None) -> AttributionEvidence:
        """
        Records a new piece of evidence and triggers a recalculation.
        """
        ev = AttributionEvidence(
            actor_id=actor_id,
            description=description,
            is_observed_fact=is_fact,
            confidence=confidence,
            reference_id=ref_id,
            reference_type=ref_type
        )
        self.db.add(ev)
        self.db.commit()
        
        # Recalculate
        new_conf = self.calculate_actor_confidence(actor_id)
        actor = self.db.query(ThreatActor).filter(ThreatActor.id == actor_id).first()
        if actor:
            actor.confidence = new_conf
            self.db.commit()
            
        self.db.refresh(ev)
        return ev

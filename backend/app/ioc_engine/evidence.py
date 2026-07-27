from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.threat_intel import IndicatorCorrelation, CorrelationEvidence

class EvidenceEngine:
    """
    Generates supporting evidence for IOC relationships.
    """

    def __init__(self, db: Session):
        self.db = db

    def generate_evidence(self, relationship: IndicatorCorrelation, source_system: str, description: str, data: Dict[str, Any]) -> CorrelationEvidence:
        """
        Creates a single piece of evidence.
        """
        evidence = CorrelationEvidence(
            relationship_id=relationship.id,
            evidence_type=self._determine_evidence_type(relationship),
            description=description,
            evidence_data=data,
            source_system=source_system
        )
        self.db.add(evidence)
        return evidence
        
    def _determine_evidence_type(self, relationship: IndicatorCorrelation) -> str:
        if relationship.correlation_type == "Exact Match":
            return "Value Equivalence"
        elif relationship.correlation_type == "Infrastructure Sharing":
            return "Infrastructure Analysis"
        return "Heuristic Analysis"

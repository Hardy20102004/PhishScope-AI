import structlog
from typing import List
from app.schemas.decision import EvidenceLinkBase

logger = structlog.get_logger("phoenix.decision.confidence")

class ConfidenceEngine:
    def calculate_confidence(self, decision_type: str, evidence: List[EvidenceLinkBase]) -> float:
        """
        Calculates a deterministic confidence score based on evidence quantity and quality.
        In reality, this would query the KG for correlation depth.
        """
        logger.info("calculating_confidence", evidence_count=len(evidence))
        
        base_score = 0.4
        
        # Quantity heuristic
        if len(evidence) >= 5:
            base_score += 0.2
        elif len(evidence) >= 2:
            base_score += 0.1
            
        # Quality heuristic
        has_kg = any(e.source_type == "KNOWLEDGE_GRAPH" for e in evidence)
        has_rag = any(e.source_type == "RAG_DOCUMENT" for e in evidence)
        
        if has_kg and has_rag:
            base_score += 0.3
        elif has_kg:
            base_score += 0.15
            
        return min(base_score, 0.98) # Never 1.0 (always some uncertainty)

from typing import Any, List

import structlog

from app.schemas.xai import ConfidenceFactor

logger = structlog.get_logger("phoenix.xai.confidence")

class ConfidenceExplanationEngine:
    def break_down_confidence(self, raw_confidence: float, raw_evidence: List[Any]) -> List[ConfidenceFactor]:
        """
        Translates a float confidence score into a breakdown of factors.
        """
        logger.info("breaking_down_confidence", raw=raw_confidence)
        
        factors = []
        
        # Base
        factors.append(ConfidenceFactor(
            factor="Base Algorithm Probability",
            impact=0.4,
            description="The baseline confidence output from the underlying heuristic model."
        ))
        
        has_kg = any(e.source_type == "KNOWLEDGE_GRAPH" for e in raw_evidence)
        if has_kg:
            factors.append(ConfidenceFactor(
                factor="Knowledge Graph Agreement",
                impact=0.3,
                description="High confidence boost due to multi-hop correlations in the internal graph."
            ))
            
        qty = len(raw_evidence)
        if qty >= 5:
            factors.append(ConfidenceFactor(
                factor="Evidence Density",
                impact=0.2,
                description="High volume of corroborating evidence across multiple domains."
            ))
        elif qty >= 2:
            factors.append(ConfidenceFactor(
                factor="Evidence Density",
                impact=0.1,
                description="Multiple pieces of evidence corroborate the conclusion."
            ))
            
        return factors

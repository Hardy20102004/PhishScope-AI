from typing import List

import structlog

from app.schemas.decision import RecommendationItem

logger = structlog.get_logger("phoenix.decision.recommendation")

class RecommendationEngine:
    def generate_recommendations(self, decision_type: str, confidence: float) -> List[RecommendationItem]:
        logger.info("generating_recommendations", decision_type=decision_type, confidence=confidence)
        
        # MOCK IMPLEMENTATION
        recs = []
        
        if confidence < 0.7:
            recs.append(RecommendationItem(
                action="COLLECT_MORE_EVIDENCE",
                priority="HIGH",
                description="Confidence is below threshold. Attempt to pull endpoint telemetry."
            ))
            
        if decision_type == "THREAT_CLASSIFICATION":
            recs.append(RecommendationItem(
                action="BLOCK_DOMAIN",
                priority="HIGH",
                description="Add secure-login.xyz to the DNS sinkhole."
            ))
            recs.append(RecommendationItem(
                action="ESCALATE_TO_TIER_3",
                priority="MEDIUM",
                description="Potential APT involvement requires senior analyst review."
            ))
            
        return recs

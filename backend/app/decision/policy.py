import structlog
from typing import List
from app.models.decision import DecisionState
from app.schemas.decision import RecommendationItem

logger = structlog.get_logger("phoenix.decision.policy")

class DecisionPolicyEngine:
    def validate_decision(self, recommendations: List[RecommendationItem], confidence: float) -> DecisionState:
        """
        Checks if the recommendations violate any organizational policies.
        e.g., auto-blocking is not allowed without human review.
        """
        logger.info("validating_decision_policy")
        
        for rec in recommendations:
            if rec.action == "BLOCK_DOMAIN" or rec.action == "ISOLATE_HOST":
                # High-impact actions require review
                logger.info("policy_check_requires_review", reason="high_impact_action", action=rec.action)
                return DecisionState.PENDING_REVIEW
                
        if confidence < 0.8:
            logger.info("policy_check_requires_review", reason="low_confidence", confidence=confidence)
            return DecisionState.PENDING_REVIEW
            
        return DecisionState.PENDING_REVIEW # For prototype, force EVERYTHING to review

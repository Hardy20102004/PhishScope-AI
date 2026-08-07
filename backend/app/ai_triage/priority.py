import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

class PriorityEngine:
    """
    Calculates final Priority Score combining Threat Severity, Business Impact, and AI Confidence.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_priority(
        self, 
        base_threat_severity: float, 
        business_impact_score: float, 
        confidence_multiplier: float
    ) -> Dict[str, Any]:
        """
        Priority = (Threat * 0.6 + Impact * 0.4) * Confidence
        """
        raw_score = (base_threat_severity * 0.6) + (business_impact_score * 0.4)
        final_score = raw_score * confidence_multiplier
        final_score = min(final_score, 100.0)
        
        tier = "LOW"
        if final_score >= 85:
            tier = "CRITICAL"
        elif final_score >= 65:
            tier = "HIGH"
        elif final_score >= 40:
            tier = "MEDIUM"
            
        return {
            "score": round(final_score, 2),
            "tier": tier
        }

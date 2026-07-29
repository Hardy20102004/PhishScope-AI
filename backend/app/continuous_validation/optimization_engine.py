import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.continuous_validation import OptimizationRecommendation

class OptimizationEngine:
    """
    Generates actionable recommendations to improve the security posture score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_recommendation(self, tenant_id: uuid.UUID, title: str, description: str, domain: str, priority: str, expected_gain: float) -> OptimizationRecommendation:
        
        rec = OptimizationRecommendation(
            tenant_id=tenant_id,
            title=title,
            description=description,
            domain=domain,
            priority=priority,
            expected_score_improvement=expected_gain
        )
        
        self.db.add(rec)
        await self.db.commit()
        await self.db.refresh(rec)
        return rec

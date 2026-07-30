import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_fusion import StrategicRecommendation

class DecisionSupportEngine:
    """
    Generates explainable, AI-assisted operational recommendations based on the unified fusion graph.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recommendations(self, tenant_id: uuid.UUID) -> List[StrategicRecommendation]:
        result = await self.db.execute(select(StrategicRecommendation).where(StrategicRecommendation.tenant_id == tenant_id))
        return result.scalars().all()

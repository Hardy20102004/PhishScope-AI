import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.itdr import ITDRRiskScore

class IdentityRiskAnalyticsEngine:
    """
    Calculates overall Identity Risk Score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_scores(self, tenant_id: uuid.UUID) -> List[ITDRRiskScore]:
        result = await self.db.execute(select(ITDRRiskScore).where(ITDRRiskScore.tenant_id == tenant_id))
        return result.scalars().all()

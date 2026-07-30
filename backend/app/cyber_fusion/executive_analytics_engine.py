import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_fusion import CrossDomainRiskScore

class ExecutiveAnalyticsEngine:
    """
    Aggregates enterprise-wide health, attack surface metrics, and executive priorities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_scores(self, tenant_id: uuid.UUID) -> List[CrossDomainRiskScore]:
        result = await self.db.execute(select(CrossDomainRiskScore).where(CrossDomainRiskScore.tenant_id == tenant_id))
        return result.scalars().all()

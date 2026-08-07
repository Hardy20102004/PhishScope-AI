import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity_intel import IdentityRiskAnalytics

class RiskEngine:
    """
    Measures identity risk, privilege risk, and operational risk.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_analytics(self, tenant_id: uuid.UUID) -> List[IdentityRiskAnalytics]:
        result = await self.db.execute(select(IdentityRiskAnalytics).where(IdentityRiskAnalytics.tenant_id == tenant_id))
        return result.scalars().all()

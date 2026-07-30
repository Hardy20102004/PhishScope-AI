import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.nhi import NHIRiskScore

class RiskEngine:
    """
    Calculates risk based on overly permissive machine identities, stale credentials, and expiring certificates.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_scores(self, tenant_id: uuid.UUID) -> List[NHIRiskScore]:
        result = await self.db.execute(select(NHIRiskScore).where(NHIRiskScore.tenant_id == tenant_id))
        return result.scalars().all()

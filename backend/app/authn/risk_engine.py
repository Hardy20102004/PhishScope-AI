import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.authn import AuthnRiskScore

class RiskEngine:
    """
    Calculates authentication risks such as weak MFA, legacy protocols, or missing recovery methods.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_scores(self, tenant_id: uuid.UUID) -> List[AuthnRiskScore]:
        result = await self.db.execute(select(AuthnRiskScore).where(AuthnRiskScore.tenant_id == tenant_id))
        return result.scalars().all()

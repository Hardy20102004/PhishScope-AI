import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.federation import FederationRiskScore

class RiskEngine:
    """
    Calculates federation risks (e.g., unencrypted SAML assertions, wildcards in OAuth redirect URIs).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_scores(self, tenant_id: uuid.UUID) -> List[FederationRiskScore]:
        result = await self.db.execute(select(FederationRiskScore).where(FederationRiskScore.tenant_id == tenant_id))
        return result.scalars().all()

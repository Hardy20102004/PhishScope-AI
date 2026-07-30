import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.pam import PAMRiskScore

class PrivilegeRiskEngine:
    """
    Quantifies risk associated with highly privileged access.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_scores(self, tenant_id: uuid.UUID) -> List[PAMRiskScore]:
        result = await self.db.execute(select(PAMRiskScore).where(PAMRiskScore.tenant_id == tenant_id))
        return result.scalars().all()

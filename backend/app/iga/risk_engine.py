import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.iga import IGARiskScore

class IGARiskEngine:
    """
    Calculates governance and compliance risk scores.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_risk_scores(self, tenant_id: uuid.UUID) -> List[IGARiskScore]:
        result = await self.db.execute(select(IGARiskScore).where(IGARiskScore.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity_intel import AdaptiveTrustScore

class TrustEngine:
    """
    Calculates the Adaptive Trust Score (ATS) based on zero trust readiness and behavior.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_trust_scores(self, tenant_id: uuid.UUID) -> List[AdaptiveTrustScore]:
        result = await self.db.execute(select(AdaptiveTrustScore).where(AdaptiveTrustScore.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.itdr import ITDRBehaviorBaseline

class BehaviorAnalyticsEngine:
    """
    Analyzes authentication patterns and maintains baselines.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_baselines(self, tenant_id: uuid.UUID) -> List[ITDRBehaviorBaseline]:
        result = await self.db.execute(select(ITDRBehaviorBaseline).where(ITDRBehaviorBaseline.tenant_id == tenant_id))
        return result.scalars().all()

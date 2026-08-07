import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity_intel import BehaviorBaseline

class BehaviorEngine:
    """
    Analyzes authentication consistency, device familiarity, and application access patterns.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_baselines(self, tenant_id: uuid.UUID) -> List[BehaviorBaseline]:
        result = await self.db.execute(select(BehaviorBaseline).where(BehaviorBaseline.tenant_id == tenant_id))
        return result.scalars().all()

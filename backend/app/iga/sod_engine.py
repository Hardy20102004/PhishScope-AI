import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.iga import IGASegregationOfDutiesRule, IGASoDViolation

class SoDEngine:
    """
    Evaluates Segregation of Duties rules.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_rules(self, tenant_id: uuid.UUID) -> List[IGASegregationOfDutiesRule]:
        result = await self.db.execute(select(IGASegregationOfDutiesRule).where(IGASegregationOfDutiesRule.tenant_id == tenant_id))
        return result.scalars().all()

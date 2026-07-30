import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_resilience import BusinessServiceNode

class BusinessContinuityEngine:
    """
    Evaluates critical business services, recovery priorities, and tracks active BCPs.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_services(self, tenant_id: uuid.UUID) -> List[BusinessServiceNode]:
        result = await self.db.execute(select(BusinessServiceNode).where(BusinessServiceNode.tenant_id == tenant_id))
        return result.scalars().all()

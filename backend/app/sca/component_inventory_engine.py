import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sca import SCADependency

class ComponentInventoryEngine:
    """
    Maintains the central asset catalog of third-party software across the enterprise.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_enterprise_inventory(self, tenant_id: uuid.UUID) -> List[SCADependency]:
        stmt = select(SCADependency).where(SCADependency.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

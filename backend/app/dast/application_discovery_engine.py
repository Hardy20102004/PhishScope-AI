import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.dast import DASTTarget
from app.schemas.dast import DASTTargetCreate

class ApplicationDiscoveryEngine:
    """
    Manages the inventory of web properties, API endpoints, and authenticated workflows.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_target(self, tenant_id: uuid.UUID, target_in: DASTTargetCreate) -> DASTTarget:
        target = DASTTarget(
            tenant_id=tenant_id,
            application_id=target_in.application_id,
            name=target_in.name,
            base_url=target_in.base_url,
            target_type=target_in.target_type,
            auth_method=target_in.auth_method
        )
        self.db.add(target)
        await self.db.commit()
        await self.db.refresh(target)
        return target

    async def get_target(self, target_id: uuid.UUID) -> Optional[DASTTarget]:
        stmt = select(DASTTarget).where(DASTTarget.id == target_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_targets(self, tenant_id: uuid.UUID) -> List[DASTTarget]:
        stmt = select(DASTTarget).where(DASTTarget.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

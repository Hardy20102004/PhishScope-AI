import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.federation import FederatedProvider

class DiscoveryEngine:
    """
    Scans and discovers Identity Providers, Service Providers, and configured apps.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_providers(self, tenant_id: uuid.UUID) -> List[FederatedProvider]:
        result = await self.db.execute(select(FederatedProvider).where(FederatedProvider.tenant_id == tenant_id))
        return result.scalars().all()

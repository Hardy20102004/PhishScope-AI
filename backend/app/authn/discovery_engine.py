import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.authn import AuthnMethod

class DiscoveryEngine:
    """
    Scans and discovers registered authentication methods across enterprise identity providers.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_methods(self, tenant_id: uuid.UUID) -> List[AuthnMethod]:
        result = await self.db.execute(select(AuthnMethod).where(AuthnMethod.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.pam import PAMCredentialLifecycle

class CredentialLifecycleEngine:
    """
    Governs vault credential lifecycles.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_credentials(self, tenant_id: uuid.UUID) -> List[PAMCredentialLifecycle]:
        result = await self.db.execute(select(PAMCredentialLifecycle).where(PAMCredentialLifecycle.tenant_id == tenant_id))
        return result.scalars().all()

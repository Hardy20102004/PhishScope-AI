import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.authn import AuthnPolicy

class PolicyEngine:
    """
    Evaluates if identities comply with enterprise authentication policies.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_policies(self, tenant_id: uuid.UUID) -> List[AuthnPolicy]:
        result = await self.db.execute(select(AuthnPolicy).where(AuthnPolicy.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.authn import AuthnAssuranceLevel

class AssuranceEngine:
    """
    Calculates Authentication Assurance Levels (AAL) based on NIST SP 800-63B guidelines.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_assurance_levels(self, tenant_id: uuid.UUID) -> List[AuthnAssuranceLevel]:
        result = await self.db.execute(select(AuthnAssuranceLevel).where(AuthnAssuranceLevel.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.federation import FederationTrust

class TrustEngine:
    """
    Analyzes cross-domain trust relationships (e.g., B2B, B2C).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_trusts(self, tenant_id: uuid.UUID) -> List[FederationTrust]:
        result = await self.db.execute(select(FederationTrust).where(FederationTrust.tenant_id == tenant_id))
        return result.scalars().all()

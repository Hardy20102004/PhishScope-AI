import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.nhi import NHITrustRelationship

class TrustRelationshipEngine:
    """
    Analyzes cross-account, federated, and inter-service trust relationships.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_relationships(self, tenant_id: uuid.UUID) -> List[NHITrustRelationship]:
        result = await self.db.execute(select(NHITrustRelationship).where(NHITrustRelationship.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.federation import FederationCertificate

class MetadataEngine:
    """
    Manages and verifies the freshness of federation metadata XML and signing certificates.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_certificates(self, tenant_id: uuid.UUID) -> List[FederationCertificate]:
        result = await self.db.execute(select(FederationCertificate).where(FederationCertificate.tenant_id == tenant_id))
        return result.scalars().all()

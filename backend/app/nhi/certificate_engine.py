import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.nhi import NHICertificate

class CertificateEngine:
    """
    Manages the inventory, expiration tracking, and trust chains of certificates.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_certificates(self, tenant_id: uuid.UUID) -> List[NHICertificate]:
        result = await self.db.execute(select(NHICertificate).where(NHICertificate.tenant_id == tenant_id))
        return result.scalars().all()

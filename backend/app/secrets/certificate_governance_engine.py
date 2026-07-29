import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.secrets import SecretMetadata, SecretType

class CertificateGovernanceEngine:
    """
    Specializes in tracking X.509/TLS certificates and alerting on impending expirations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_certificates(self, tenant_id: uuid.UUID) -> List[SecretMetadata]:
        stmt = select(SecretMetadata).where(
            SecretMetadata.tenant_id == tenant_id,
            SecretMetadata.secret_type == SecretType.TLS_CERTIFICATE
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

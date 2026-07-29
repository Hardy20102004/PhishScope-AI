import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.secrets import SecretMetadata
from app.schemas.secrets import SecretMetadataCreate

class SecretsDiscoveryEngine:
    """
    Catalog mechanism that tracks secrets found in source code, CI/CD, and vaults (metadata only).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_secret_metadata(self, tenant_id: uuid.UUID, secret_in: SecretMetadataCreate) -> SecretMetadata:
        secret = SecretMetadata(
            tenant_id=tenant_id,
            secret_type=secret_in.secret_type,
            name=secret_in.name,
            identifier_hash=secret_in.identifier_hash,
            location_uri=secret_in.location_uri,
            lifecycle_status=secret_in.lifecycle_status,
            expires_at=secret_in.expires_at,
            last_rotated_at=secret_in.last_rotated_at,
            owner=secret_in.owner
        )
        self.db.add(secret)
        await self.db.commit()
        await self.db.refresh(secret)
        return secret

    async def list_secrets(self, tenant_id: uuid.UUID) -> List[SecretMetadata]:
        stmt = select(SecretMetadata).where(SecretMetadata.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

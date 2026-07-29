import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sbom import SoftwareArtifact
from app.schemas.sbom import SoftwareArtifactCreate

class ArtifactInventoryEngine:
    """
    Catalogs applications, container images, and release artifacts.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_artifact(self, tenant_id: uuid.UUID, artifact_in: SoftwareArtifactCreate) -> SoftwareArtifact:
        artifact = SoftwareArtifact(
            tenant_id=tenant_id,
            sbom_id=artifact_in.sbom_id,
            name=artifact_in.name,
            type=artifact_in.type,
            version=artifact_in.version,
            purl=artifact_in.purl,
            hash_sha256=artifact_in.hash_sha256
        )
        self.db.add(artifact)
        await self.db.commit()
        await self.db.refresh(artifact)
        return artifact

    async def list_artifacts(self, tenant_id: uuid.UUID) -> List[SoftwareArtifact]:
        stmt = select(SoftwareArtifact).where(SoftwareArtifact.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sbom import SoftwareDependency
from app.schemas.sbom import SoftwareDependencyCreate

class DependencyDiscoveryEngine:
    """
    Builds and maintains the internal dependency tree (Direct vs. Transitive).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_dependency(self, tenant_id: uuid.UUID, dep_in: SoftwareDependencyCreate) -> SoftwareDependency:
        dep = SoftwareDependency(
            tenant_id=tenant_id,
            sbom_id=dep_in.sbom_id,
            name=dep_in.name,
            version=dep_in.version,
            purl=dep_in.purl,
            is_direct=dep_in.is_direct,
            license=dep_in.license,
            is_end_of_life=dep_in.is_end_of_life
        )
        self.db.add(dep)
        await self.db.commit()
        await self.db.refresh(dep)
        return dep

    async def list_dependencies(self, tenant_id: uuid.UUID) -> List[SoftwareDependency]:
        stmt = select(SoftwareDependency).where(SoftwareDependency.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

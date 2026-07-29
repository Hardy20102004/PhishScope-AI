import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sca import SCADependency
from app.schemas.sca import SCADependencyCreate

class DependencyDiscoveryEngine:
    """
    Parses manifests and lockfiles to construct dependency trees.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_dependency(self, tenant_id: uuid.UUID, dep_in: SCADependencyCreate) -> SCADependency:
        dep = SCADependency(
            tenant_id=tenant_id,
            application_id=dep_in.application_id,
            package_intelligence_id=dep_in.package_intelligence_id,
            parent_dependency_id=dep_in.parent_dependency_id,
            ecosystem=dep_in.ecosystem,
            package_name=dep_in.package_name,
            version_constraint=dep_in.version_constraint,
            resolved_version=dep_in.resolved_version,
            dependency_type=dep_in.dependency_type
        )
        self.db.add(dep)
        await self.db.commit()
        await self.db.refresh(dep)
        return dep

    async def list_dependencies(self, tenant_id: uuid.UUID) -> List[SCADependency]:
        stmt = select(SCADependency).where(SCADependency.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

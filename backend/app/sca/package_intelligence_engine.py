import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sca import SCAPackageIntelligence
from app.schemas.sca import SCAPackageIntelligenceCreate

class PackageIntelligenceEngine:
    """
    Correlates discovered dependencies with open-source threat intelligence and community health metrics.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_package_intelligence(self, tenant_id: uuid.UUID, pkg_in: SCAPackageIntelligenceCreate) -> SCAPackageIntelligence:
        pkg = SCAPackageIntelligence(
            tenant_id=tenant_id,
            ecosystem=pkg_in.ecosystem,
            package_name=pkg_in.package_name,
            version=pkg_in.version,
            is_deprecated=pkg_in.is_deprecated,
            is_abandoned=pkg_in.is_abandoned,
            end_of_life_date=pkg_in.end_of_life_date,
            popularity_score=pkg_in.popularity_score,
            maintenance_score=pkg_in.maintenance_score,
            known_cves=pkg_in.known_cves
        )
        self.db.add(pkg)
        await self.db.commit()
        await self.db.refresh(pkg)
        return pkg

    async def get_package(self, package_id: uuid.UUID) -> Optional[SCAPackageIntelligence]:
        stmt = select(SCAPackageIntelligence).where(SCAPackageIntelligence.id == package_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

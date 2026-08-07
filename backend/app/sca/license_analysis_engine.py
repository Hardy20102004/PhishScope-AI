import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sca import SCALicense
from app.schemas.sca import SCALicenseCreate

class LicenseAnalysisEngine:
    """
    Evaluates open source licenses against defined enterprise policies to flag copyleft or unapproved licenses.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_license(self, tenant_id: uuid.UUID, license_in: SCALicenseCreate) -> SCALicense:
        lic = SCALicense(
            tenant_id=tenant_id,
            package_intelligence_id=license_in.package_intelligence_id,
            spdx_id=license_in.spdx_id,
            is_copyleft=license_in.is_copyleft,
            is_approved=license_in.is_approved
        )
        self.db.add(lic)
        await self.db.commit()
        await self.db.refresh(lic)
        return lic

    async def list_licenses(self, tenant_id: uuid.UUID) -> List[SCALicense]:
        stmt = select(SCALicense).where(SCALicense.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

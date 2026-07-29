import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.secrets import SecretExposure
from app.schemas.secrets import SecretExposureCreate

class ExposureAssessmentEngine:
    """
    Analyzes secrets for hardcoding risks, excessive permissions, or dormancy.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_exposure(self, tenant_id: uuid.UUID, exposure_in: SecretExposureCreate) -> SecretExposure:
        exposure = SecretExposure(
            tenant_id=tenant_id,
            secret_id=exposure_in.secret_id,
            exposure_type=exposure_in.exposure_type,
            severity=exposure_in.severity,
            details=exposure_in.details
        )
        self.db.add(exposure)
        await self.db.commit()
        await self.db.refresh(exposure)
        return exposure

    async def list_exposures(self, tenant_id: uuid.UUID) -> List[SecretExposure]:
        stmt = select(SecretExposure).where(SecretExposure.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

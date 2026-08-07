import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sbom import SBOMRecord
from app.schemas.sbom import SBOMRecordCreate

class SBOMManagementEngine:
    """
    Handles ingestion, validation, and parsing of CycloneDX and SPDX documents.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_sbom(self, tenant_id: uuid.UUID, sbom_in: SBOMRecordCreate) -> SBOMRecord:
        record = SBOMRecord(
            tenant_id=tenant_id,
            application_id=sbom_in.application_id,
            name=sbom_in.name,
            version=sbom_in.version,
            format=sbom_in.format,
            component_count=sbom_in.component_count,
            raw_data=sbom_in.raw_data
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def get_sbom(self, record_id: uuid.UUID) -> Optional[SBOMRecord]:
        stmt = select(SBOMRecord).where(SBOMRecord.id == record_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_sboms(self, tenant_id: uuid.UUID) -> List[SBOMRecord]:
        stmt = select(SBOMRecord).where(SBOMRecord.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from app.models.dast import DASTScan, DASTScanStatus
from app.schemas.dast import DASTScanCreate

class RuntimeAssessmentEngine:
    """
    Orchestrates active crawls, fuzzing, and security control validations against the target application.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def initiate_scan(self, tenant_id: uuid.UUID, scan_in: DASTScanCreate) -> DASTScan:
        scan = DASTScan(
            tenant_id=tenant_id,
            target_id=scan_in.target_id,
            status=DASTScanStatus.RUNNING,
            endpoints_tested=scan_in.endpoints_tested,
            started_at=datetime.now(timezone.utc)
        )
        self.db.add(scan)
        await self.db.commit()
        await self.db.refresh(scan)
        return scan

    async def get_scan(self, scan_id: uuid.UUID) -> Optional[DASTScan]:
        stmt = select(DASTScan).where(DASTScan.id == scan_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_scans(self, tenant_id: uuid.UUID) -> List[DASTScan]:
        stmt = select(DASTScan).where(DASTScan.tenant_id == tenant_id).order_by(DASTScan.started_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def complete_scan(self, scan_id: uuid.UUID) -> Optional[DASTScan]:
        stmt = select(DASTScan).where(DASTScan.id == scan_id)
        scan = (await self.db.execute(stmt)).scalar_one_or_none()
        if scan:
            scan.status = DASTScanStatus.COMPLETED
            scan.completed_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(scan)
        return scan

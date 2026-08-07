import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sast import SASTScan, ScanStatus
from app.schemas.sast import SASTScanCreate
from datetime import datetime, timezone

class SourceAnalysisEngine:
    """
    Orchestrates the ingestion of source code context and schedules scans.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def initiate_scan(self, tenant_id: uuid.UUID, scan_in: SASTScanCreate) -> SASTScan:
        scan = SASTScan(
            tenant_id=tenant_id,
            repository_id=scan_in.repository_id,
            branch=scan_in.branch,
            commit_sha=scan_in.commit_sha,
            status=ScanStatus.RUNNING,
            files_scanned=scan_in.files_scanned,
            lines_of_code=scan_in.lines_of_code,
            started_at=datetime.now(timezone.utc)
        )
        self.db.add(scan)
        await self.db.commit()
        await self.db.refresh(scan)
        return scan

    async def get_scan(self, scan_id: uuid.UUID) -> Optional[SASTScan]:
        stmt = select(SASTScan).where(SASTScan.id == scan_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_scans(self, tenant_id: uuid.UUID) -> List[SASTScan]:
        stmt = select(SASTScan).where(SASTScan.tenant_id == tenant_id).order_by(SASTScan.started_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def complete_scan(self, scan_id: uuid.UUID) -> Optional[SASTScan]:
        stmt = select(SASTScan).where(SASTScan.id == scan_id)
        scan = (await self.db.execute(stmt)).scalar_one_or_none()
        if scan:
            scan.status = ScanStatus.COMPLETED
            scan.completed_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(scan)
        return scan

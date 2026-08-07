import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.appsec_command_center import AppSecConsolidatedFinding
from app.schemas.appsec_command_center import AppSecConsolidatedFindingCreate

class AppSecCommandCenterManager:
    """
    Orchestrator that aggregates findings across the AppSec toolchain.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_finding(self, tenant_id: uuid.UUID, finding_in: AppSecConsolidatedFindingCreate) -> AppSecConsolidatedFinding:
        finding = AppSecConsolidatedFinding(
            tenant_id=tenant_id,
            application_id=finding_in.application_id,
            source_scanner=finding_in.source_scanner,
            severity=finding_in.severity,
            cwe_id=finding_in.cwe_id,
            title=finding_in.title,
            description=finding_in.description,
            is_remediated=finding_in.is_remediated
        )
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

    async def list_findings(self, tenant_id: uuid.UUID) -> List[AppSecConsolidatedFinding]:
        stmt = select(AppSecConsolidatedFinding).where(AppSecConsolidatedFinding.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

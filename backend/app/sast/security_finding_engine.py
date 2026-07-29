import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sast import SASTFinding, SASTRule
from app.schemas.sast import SASTFindingCreate

class SecurityFindingEngine:
    """
    Normalizes, deduplicates, and manages the lifecycle of SASTFinding records.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_finding(self, tenant_id: uuid.UUID, finding_in: SASTFindingCreate) -> SASTFinding:
        finding = SASTFinding(
            tenant_id=tenant_id,
            scan_id=finding_in.scan_id,
            rule_id=finding_in.rule_id,
            file_path=finding_in.file_path,
            line_number=finding_in.line_number,
            code_snippet=finding_in.code_snippet,
            severity=finding_in.severity,
            exploitability_score=finding_in.exploitability_score,
            is_suppressed=finding_in.is_suppressed
        )
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

    async def list_findings(self, tenant_id: uuid.UUID) -> List[SASTFinding]:
        stmt = select(SASTFinding).where(SASTFinding.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

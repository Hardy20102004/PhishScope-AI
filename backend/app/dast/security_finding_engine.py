import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.dast import DASTFinding
from app.schemas.dast import DASTFindingCreate

class SecurityFindingEngine:
    """
    Aggregates, deduplicates, and manages the lifecycle of dynamic vulnerabilities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_finding(self, tenant_id: uuid.UUID, finding_in: DASTFindingCreate) -> DASTFinding:
        finding = DASTFinding(
            tenant_id=tenant_id,
            scan_id=finding_in.scan_id,
            vulnerability_name=finding_in.vulnerability_name,
            cwe=finding_in.cwe,
            url=finding_in.url,
            method=finding_in.method,
            request_payload=finding_in.request_payload,
            response_snippet=finding_in.response_snippet,
            severity=finding_in.severity,
            exploitability_score=finding_in.exploitability_score,
            is_suppressed=finding_in.is_suppressed
        )
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

    async def list_findings(self, tenant_id: uuid.UUID) -> List[DASTFinding]:
        stmt = select(DASTFinding).where(DASTFinding.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

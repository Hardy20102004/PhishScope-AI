import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.aspm import SecurityFinding, ApplicationRisk
from app.schemas.aspm import SecurityFindingCreate

class PostureAnalyticsEngine:
    """
    Ingests and analyzes security findings (SAST, SCA, DAST, etc.) across the enterprise.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_finding(self, tenant_id: uuid.UUID, finding_in: SecurityFindingCreate) -> SecurityFinding:
        finding = SecurityFinding(
            tenant_id=tenant_id,
            application_id=finding_in.application_id,
            repository_id=finding_in.repository_id,
            finding_type=finding_in.finding_type,
            severity=finding_in.severity,
            status=finding_in.status,
            title=finding_in.title,
            description=finding_in.description,
            cve_id=finding_in.cve_id,
            file_path=finding_in.file_path,
            line_number=finding_in.line_number,
            scanner_name=finding_in.scanner_name
        )
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

    async def get_findings_for_application(self, app_id: uuid.UUID) -> List[SecurityFinding]:
        stmt = select(SecurityFinding).where(SecurityFinding.application_id == app_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_posture_summary(self, tenant_id: uuid.UUID) -> dict:
        """
        Calculates total findings by severity and type for a tenant.
        """
        stmt = select(SecurityFinding.severity, func.count(SecurityFinding.id)).where(
            SecurityFinding.tenant_id == tenant_id
        ).group_by(SecurityFinding.severity)
        
        res = await self.db.execute(stmt)
        counts = {row[0].value: row[1] for row in res.all()}
        
        return {
            "critical": counts.get("CRITICAL", 0),
            "high": counts.get("HIGH", 0),
            "medium": counts.get("MEDIUM", 0),
            "low": counts.get("LOW", 0)
        }

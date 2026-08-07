import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.iac import IaCConfigurationFinding
from app.schemas.iac import IaCConfigurationFindingCreate

class TemplateAnalysisEngine:
    """
    Analyzes HCL/YAML/JSON syntax and semantics to identify findings.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_finding(self, tenant_id: uuid.UUID, finding_in: IaCConfigurationFindingCreate) -> IaCConfigurationFinding:
        finding = IaCConfigurationFinding(
            tenant_id=tenant_id,
            template_id=finding_in.template_id,
            severity=finding_in.severity,
            category=finding_in.category,
            title=finding_in.title,
            description=finding_in.description,
            resource_id=finding_in.resource_id,
            line_number=finding_in.line_number
        )
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

    async def list_findings(self, tenant_id: uuid.UUID) -> List[IaCConfigurationFinding]:
        stmt = select(IaCConfigurationFinding).where(IaCConfigurationFinding.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

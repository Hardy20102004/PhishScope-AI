import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cspm import ComplianceFinding

class ComplianceEngine:
    """
    Maps identified misconfigurations back to specific compliance frameworks.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_compliance_finding(self, tenant_id: uuid.UUID, framework: str, control: str, passed: int, failed: int) -> ComplianceFinding:
        finding = ComplianceFinding(
            tenant_id=tenant_id,
            framework=framework,
            control_id=control,
            passed=passed,
            failed=failed
        )
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

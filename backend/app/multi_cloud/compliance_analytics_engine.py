import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.multi_cloud import ComplianceTrend

class ComplianceAnalyticsEngine:
    """
    Aggregates compliance findings across all cloud providers.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_trend(self, tenant_id: uuid.UUID, framework: str, percentage: float, failed: int) -> ComplianceTrend:
        trend = ComplianceTrend(
            tenant_id=tenant_id,
            framework=framework,
            compliance_percentage=percentage,
            failed_controls=failed
        )
        self.db.add(trend)
        await self.db.commit()
        await self.db.refresh(trend)
        return trend

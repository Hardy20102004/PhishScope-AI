import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cyber_resilience import ExecutiveKPI

class ExecutiveKPIEngine:
    """
    Calculates specific Key Performance Indicators required for executive reporting.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_kpi(self, tenant_id: uuid.UUID, name: str, value: float, unit: str, trend: str) -> ExecutiveKPI:
        kpi = ExecutiveKPI(
            tenant_id=tenant_id,
            metric_name=name,
            metric_value=value,
            metric_unit=unit,
            trend=trend
        )
        self.db.add(kpi)
        await self.db.commit()
        await self.db.refresh(kpi)
        return kpi

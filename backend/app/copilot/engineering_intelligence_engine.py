import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.copilot import EngineeringMetric
from app.schemas.copilot import EngineeringMetricCreate

class EngineeringIntelligenceEngine:
    """
    Calculates macro-level project health and technical debt metrics.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_metric(self, tenant_id: uuid.UUID, metric_in: EngineeringMetricCreate) -> EngineeringMetric:
        metric = EngineeringMetric(
            tenant_id=tenant_id,
            project_name=metric_in.project_name,
            technical_debt_score=metric_in.technical_debt_score,
            security_trend_score=metric_in.security_trend_score
        )
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def get_metrics(self, tenant_id: uuid.UUID) -> List[EngineeringMetric]:
        stmt = select(EngineeringMetric).where(EngineeringMetric.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

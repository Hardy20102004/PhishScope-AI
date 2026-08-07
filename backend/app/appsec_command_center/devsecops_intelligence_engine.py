import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.appsec_command_center import EngineeringProductivityMetric
from app.schemas.appsec_command_center import EngineeringProductivityMetricCreate

class DevSecOpsIntelligenceEngine:
    """
    Analyzes developer metrics and security friction.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_metric(self, tenant_id: uuid.UUID, metric_in: EngineeringProductivityMetricCreate) -> EngineeringProductivityMetric:
        metric = EngineeringProductivityMetric(
            tenant_id=tenant_id,
            application_id=metric_in.application_id,
            mean_time_to_remediate_days=metric_in.mean_time_to_remediate_days,
            deployment_frequency_per_week=metric_in.deployment_frequency_per_week,
            security_friction_score=metric_in.security_friction_score
        )
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def get_metrics(self, tenant_id: uuid.UUID) -> List[EngineeringProductivityMetric]:
        stmt = select(EngineeringProductivityMetric).where(EngineeringProductivityMetric.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

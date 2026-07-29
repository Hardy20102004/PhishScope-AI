import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.executive_intelligence import GovernanceMetric

class GovernanceAnalyticsEngine:
    """
    Aggregates compliance status and roadmap completion metrics.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_governance_metric(self, tenant_id: uuid.UUID, framework: str, name: str, score: float) -> GovernanceMetric:
        metric = GovernanceMetric(
            tenant_id=tenant_id,
            framework=framework,
            metric_name=name,
            compliance_score=score
        )
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

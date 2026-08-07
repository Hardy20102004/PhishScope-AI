import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.detection_gap import MitreCoverageMetric

class CoverageAnalysisEngine:
    """
    Calculates the overall enterprise MITRE ATT&CK coverage by aggregating individual technique metrics.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_coverage_metric(self, tenant_id: uuid.UUID, tactic: str, tech_id: str, tech_name: str, score: float) -> MitreCoverageMetric:
        metric = MitreCoverageMetric(
            tenant_id=tenant_id,
            tactic_id=tactic,
            technique_id=tech_id,
            technique_name=tech_name,
            coverage_score=score
        )
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def get_overall_coverage(self, tenant_id: uuid.UUID) -> float:
        res = await self.db.execute(select(MitreCoverageMetric).where(MitreCoverageMetric.tenant_id == tenant_id))
        metrics = res.scalars().all()
        
        if not metrics:
            return 0.0
            
        total = sum(m.coverage_score for m in metrics)
        return total / len(metrics)

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.detection_gap import MitreCoverageMetric, DetectionGapRecord

class GapAnalysisEngine:
    """
    Identifies techniques where coverage falls below an acceptable threshold.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_gaps(self, tenant_id: uuid.UUID) -> list[DetectionGapRecord]:
        res = await self.db.execute(select(MitreCoverageMetric).where(MitreCoverageMetric.tenant_id == tenant_id))
        metrics = res.scalars().all()
        
        gaps = []
        for metric in metrics:
            if metric.coverage_score < 30.0:
                gap = DetectionGapRecord(
                    tenant_id=tenant_id,
                    technique_id=metric.technique_id,
                    severity="CRITICAL" if metric.coverage_score == 0.0 else "HIGH",
                    description=f"Coverage for {metric.technique_name} is critically low ({metric.coverage_score}%)."
                )
                self.db.add(gap)
                gaps.append(gap)
                
        if gaps:
            await self.db.commit()
            for g in gaps:
                await self.db.refresh(g)
                
        return gaps

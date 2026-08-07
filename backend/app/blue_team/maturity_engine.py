import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.blue_team import ReadinessSnapshot, DetectionMetric, AnalystTeamMetric

class MaturityEngine:
    """
    Synthesizes discrete metrics (detections, analyst speeds) into a unified Operational Maturity score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_maturity_score(self, tenant_id: uuid.UUID) -> ReadinessSnapshot:
        # Pull latest detection metrics
        res_det = await self.db.execute(select(DetectionMetric).where(DetectionMetric.tenant_id == tenant_id))
        detections = res_det.scalars().all()
        
        # Pull latest analyst metrics
        res_an = await self.db.execute(select(AnalystTeamMetric).where(AnalystTeamMetric.tenant_id == tenant_id))
        analyst_metrics = res_an.scalars().all()
        
        # Scoring Logic (Simplified for prototype)
        det_score = 0.0
        if detections:
            noisy_rules = sum(1 for d in detections if d.status == "NOISY")
            det_score = max(0.0, 100.0 - ((noisy_rules / len(detections)) * 100.0))
            
        an_score = 0.0
        if analyst_metrics:
            # e.g., target MTT is < 15 mins.
            avg_mtt = sum(a.mean_time_to_triage_mins for a in analyst_metrics) / len(analyst_metrics)
            an_score = max(0.0, 100.0 - (avg_mtt)) # rough abstraction
            
        overall = (det_score * 0.5) + (an_score * 0.5)
        
        snapshot = ReadinessSnapshot(
            tenant_id=tenant_id,
            overall_maturity_score=overall,
            detection_health_score=det_score,
            analyst_readiness_score=an_score,
            aggregated_metrics={
                "total_rules_evaluated": len(detections),
                "total_teams_evaluated": len(analyst_metrics)
            }
        )
        
        self.db.add(snapshot)
        await self.db.commit()
        await self.db.refresh(snapshot)
        return snapshot

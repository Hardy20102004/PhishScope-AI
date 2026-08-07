import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cwpp import WorkloadRiskScore, BehaviorAnomaly
from sqlalchemy import select

class WorkloadRiskEngine:
    """
    Aggregates runtime anomalies to calculate the overall risk posture of a workload.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_risk_score(self, tenant_id: uuid.UUID, workload_id: uuid.UUID) -> WorkloadRiskScore:
        # Get all anomalies for workload
        res = await self.db.execute(select(BehaviorAnomaly).where(BehaviorAnomaly.workload_id == workload_id))
        anomalies = res.scalars().all()
        
        score = 0.0
        for a in anomalies:
            if a.severity == "CRITICAL": score += 50.0
            elif a.severity == "HIGH": score += 20.0
            
        score = min(score, 100.0) # Cap at 100
        
        # Check if record exists
        res = await self.db.execute(select(WorkloadRiskScore).where(WorkloadRiskScore.workload_id == workload_id))
        risk_record = res.scalars().first()
        
        if not risk_record:
            risk_record = WorkloadRiskScore(tenant_id=tenant_id, workload_id=workload_id, risk_score=score)
            self.db.add(risk_record)
        else:
            risk_record.risk_score = score
            
        await self.db.commit()
        await self.db.refresh(risk_record)
        return risk_record

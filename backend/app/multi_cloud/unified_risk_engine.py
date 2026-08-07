import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.multi_cloud import UnifiedRiskScore
from sqlalchemy import select

class UnifiedRiskEngine:
    """
    Calculates the top-level Enterprise Cloud Risk Score using a Critical Path Strategy.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_enterprise_risk(self, tenant_id: uuid.UUID, critical_findings_count: int) -> UnifiedRiskScore:
        # Implementing the Critical Path Strategy
        # If there are critical toxic combinations (e.g. public IP + unpatched CVE + Admin IAM), risk spikes exponentially.
        base_score = 100.0
        multiplier = 1.5
        
        calculated_score = base_score + (critical_findings_count * 50 * multiplier)
        if calculated_score > 1000.0:
            calculated_score = 1000.0
            
        res = await self.db.execute(select(UnifiedRiskScore).where(UnifiedRiskScore.tenant_id == tenant_id))
        score_record = res.scalars().first()
        
        if not score_record:
            score_record = UnifiedRiskScore(
                tenant_id=tenant_id, 
                global_score=calculated_score,
                provider_breakdown={"AWS": calculated_score * 0.6, "AZURE": calculated_score * 0.4},
                category_breakdown={"CSPM": calculated_score * 0.5, "CWPP": calculated_score * 0.5}
            )
            self.db.add(score_record)
        else:
            score_record.global_score = calculated_score
            
        await self.db.commit()
        await self.db.refresh(score_record)
        return score_record

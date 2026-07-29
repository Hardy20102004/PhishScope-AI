import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_resilience import CyberResilienceScore

class SecurityScoringEngine:
    """
    Aggregates technical scores into the final board-level Cyber Resilience Score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_resilience_score(self, tenant_id: uuid.UUID, prev_eff: float, det_eff: float, res_eff: float) -> CyberResilienceScore:
        overall = (prev_eff * 0.4) + (det_eff * 0.3) + (res_eff * 0.3)
        
        score = CyberResilienceScore(
            tenant_id=tenant_id,
            overall_score=overall,
            preventive_effectiveness=prev_eff,
            detective_effectiveness=det_eff,
            response_effectiveness=res_eff
        )
        self.db.add(score)
        await self.db.commit()
        await self.db.refresh(score)
        return score

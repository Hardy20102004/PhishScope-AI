import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_resilience import ResilienceAssessment

class SecurityScoringEngine:
    """
    Aggregates technical scores into the final board-level Cyber Resilience Score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_resilience_score(self, tenant_id: uuid.UUID, prev_eff: float, det_eff: float, res_eff: float) -> ResilienceAssessment:
        overall = (prev_eff * 0.4) + (det_eff * 0.3) + (res_eff * 0.3)
        
        score = ResilienceAssessment(
            tenant_id=tenant_id,
            overall_readiness_score=overall,
            domain_scores={
                "preventive_effectiveness": prev_eff,
                "detective_effectiveness": det_eff,
                "response_effectiveness": res_eff
            }
        )
        self.db.add(score)
        await self.db.commit()
        await self.db.refresh(score)
        return score

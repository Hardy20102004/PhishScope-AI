import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.continuous_validation import SecurityPostureSnapshot

class SecurityPostureEngine:
    """
    Calculates the Apex Security Posture Score based on outputs from Blue, Red, and BAS platforms.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_current_posture(self, tenant_id: uuid.UUID, blue_score: float, bas_score: float, red_score: float) -> SecurityPostureSnapshot:
        # In a real system, this engine would pull directly from the other module tables.
        # For this MVP, we accept the scores directly or simulate the aggregation.
        
        # Overall posture is a weighted average of:
        # 1. Blue Team Readiness (Detection Health + Analyst Speed) [40%]
        # 2. BAS Platform (Automated Control Effectiveness) [40%]
        # 3. Red Team Results (Manual Adversarial Evasion) [20%]
        
        overall = (blue_score * 0.4) + (bas_score * 0.4) + (red_score * 0.2)
        
        snapshot = SecurityPostureSnapshot(
            tenant_id=tenant_id,
            overall_posture_score=overall,
            detection_maturity=blue_score,
            control_effectiveness=bas_score,
            response_readiness=red_score
        )
        
        self.db.add(snapshot)
        await self.db.commit()
        await self.db.refresh(snapshot)
        return snapshot

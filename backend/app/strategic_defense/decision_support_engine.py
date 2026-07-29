import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.strategic_defense import StrategicRecommendation, DecisionApprovalLog

class DecisionSupportEngine:
    """
    Manages human approval workflows for strategic recommendations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_decision(self, tenant_id: uuid.UUID, rec_id: uuid.UUID, user_id: uuid.UUID, action: str, justify: str = None) -> DecisionApprovalLog:
        # Get rec and update status
        rec = await self.db.get(StrategicRecommendation, rec_id)
        if rec:
            rec.status = action
        
        # Log approval
        log = DecisionApprovalLog(
            tenant_id=tenant_id,
            recommendation_id=rec_id,
            executive_user_id=user_id,
            action_taken=action,
            justification=justify
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

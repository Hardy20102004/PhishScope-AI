import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ctem import RemediationPlan

class RemediationPlanningEngine:
    """
    Generates a phased roadmap of fixes, optimizing for maximum risk reduction.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_plan(self, tenant_id: uuid.UUID, exposure_id: uuid.UUID, title: str, steps: dict, expected_reduction: float) -> RemediationPlan:
        plan = RemediationPlan(
            tenant_id=tenant_id,
            exposure_id=exposure_id,
            plan_title=title,
            steps=steps,
            estimated_risk_reduction=expected_reduction,
            status="PROPOSED"
        )
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

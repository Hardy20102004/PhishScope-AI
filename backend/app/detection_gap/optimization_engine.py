import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.detection_gap import ControlOptimizationPlan

class OptimizationEngine:
    """
    Recommends specific engineering tasks to remediate identified gaps.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_optimization_plan(self, tenant_id: uuid.UUID, gap_record_id: uuid.UUID, title: str, description: str, platform: str, expected_increase: float) -> ControlOptimizationPlan:
        plan = ControlOptimizationPlan(
            tenant_id=tenant_id,
            gap_record_id=gap_record_id,
            title=title,
            description=description,
            target_platform=platform,
            expected_coverage_increase=expected_increase
        )
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

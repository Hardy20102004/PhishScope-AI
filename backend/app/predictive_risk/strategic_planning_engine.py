import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.predictive_risk import StrategicPlan

class StrategicPlanningEngine:
    """
    Assists in long-term capability mapping and operational resilience planning.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_plans(self, tenant_id: uuid.UUID) -> List[StrategicPlan]:
        result = await self.db.execute(select(StrategicPlan).where(StrategicPlan.tenant_id == tenant_id))
        return result.scalars().all()

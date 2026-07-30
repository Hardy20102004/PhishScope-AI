import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.digital_twin import ResilienceMetric

class ResilienceAssessmentEngine:
    """
    Evaluates control coverage and overall resilience of the digital twin.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_metrics(self, tenant_id: uuid.UUID) -> List[ResilienceMetric]:
        result = await self.db.execute(select(ResilienceMetric).where(ResilienceMetric.tenant_id == tenant_id))
        return result.scalars().all()

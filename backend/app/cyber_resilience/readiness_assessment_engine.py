import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_resilience import ResilienceAssessment

class ReadinessAssessmentEngine:
    """
    Aggregates RTO/RPO metrics and DR test results into a unified Continuous Readiness score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_assessments(self, tenant_id: uuid.UUID) -> List[ResilienceAssessment]:
        result = await self.db.execute(select(ResilienceAssessment).where(ResilienceAssessment.tenant_id == tenant_id))
        return result.scalars().all()

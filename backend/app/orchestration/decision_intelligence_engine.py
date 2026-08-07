import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.orchestration import OrchestrationDecisionLog

class DecisionIntelligenceEngine:
    """
    Analyzes cross-domain context to provide explainable operational recommendations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_decisions(self, tenant_id: uuid.UUID) -> List[OrchestrationDecisionLog]:
        result = await self.db.execute(select(OrchestrationDecisionLog).where(OrchestrationDecisionLog.tenant_id == tenant_id))
        return result.scalars().all()


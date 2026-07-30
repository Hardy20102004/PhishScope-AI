import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.orchestration import DecisionLog

class DecisionIntelligenceEngine:
    """
    Analyzes cross-domain context to provide explainable operational recommendations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_decisions(self, tenant_id: uuid.UUID) -> List[DecisionLog]:
        result = await self.db.execute(select(DecisionLog).where(DecisionLog.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.predictive_risk import InvestmentScenario

class InvestmentPrioritizationEngine:
    """
    Evaluates capability gaps and recommends resource allocations to maximize risk reduction.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_scenarios(self, tenant_id: uuid.UUID) -> List[InvestmentScenario]:
        result = await self.db.execute(select(InvestmentScenario).where(InvestmentScenario.tenant_id == tenant_id))
        return result.scalars().all()

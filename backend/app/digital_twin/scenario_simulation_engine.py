import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.digital_twin import SimulationScenario

class ScenarioSimulationEngine:
    """
    Supports 'what-if' simulations without affecting production systems.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_simulations(self, tenant_id: uuid.UUID) -> List[SimulationScenario]:
        result = await self.db.execute(select(SimulationScenario).where(SimulationScenario.tenant_id == tenant_id))
        return result.scalars().all()

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.bas_platform import BasScenario, BasSimulation

class SimulationManager:
    """
    Orchestrates the safe execution of validation scenarios.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_scenario(self, tenant_id: uuid.UUID, name: str, description: str, tactic: str, technique_id: str, steps: list) -> BasScenario:
        scenario = BasScenario(
            tenant_id=tenant_id,
            name=name,
            description=description,
            tactic=tactic,
            technique_id=technique_id,
            execution_steps=steps
        )
        self.db.add(scenario)
        await self.db.commit()
        await self.db.refresh(scenario)
        return scenario

    async def execute_simulation(self, tenant_id: uuid.UUID, scenario_id: uuid.UUID) -> BasSimulation:
        result = await self.db.execute(select(BasScenario).where(BasScenario.id == scenario_id))
        scenario = result.scalar_one_or_none()
        if not scenario:
            raise ValueError("Scenario not found")
            
        simulation = BasSimulation(
            tenant_id=tenant_id,
            scenario_id=scenario.id,
            status="RUNNING"
        )
        self.db.add(simulation)
        await self.db.flush()
        
        # Here we would safely dispatch the steps to an agent or a benign test executable.
        # For this implementation, we will move directly to simulating the validation phase.
        
        await self.db.commit()
        await self.db.refresh(simulation)
        return simulation

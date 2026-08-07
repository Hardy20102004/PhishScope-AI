import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.bas_platform import BasSimulation, BasValidationResult

class ScoringEngine:
    """
    Calculates the overarching Security Readiness Score for a simulation.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def finalize_simulation_score(self, simulation_id: uuid.UUID) -> BasSimulation:
        
        result = await self.db.execute(select(BasSimulation).where(BasSimulation.id == simulation_id))
        simulation = result.scalar_one_or_none()
        
        if not simulation:
            raise ValueError("Simulation not found")
            
        res = await self.db.execute(select(BasValidationResult).where(BasValidationResult.simulation_id == simulation.id))
        validation_results = res.scalars().all()
        
        if not validation_results:
            simulation.overall_score = 0.0
        else:
            detected_count = sum(1 for r in validation_results if r.was_detected)
            simulation.overall_score = (detected_count / len(validation_results)) * 100.0
            
        simulation.status = "COMPLETED"
        simulation.completed_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        await self.db.refresh(simulation, ["results"])
        return simulation

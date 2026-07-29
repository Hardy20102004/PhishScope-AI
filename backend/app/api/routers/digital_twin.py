from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.models.digital_twin import SimulationScenario
from app.schemas.digital_twin import (
    SimulationScenarioCreate,
    SimulationScenarioResponse,
    SimulationResultResponse
)

from app.digital_twin.simulation_engine import SimulationEngine
from app.digital_twin.optimization_engine import OptimizationEngine

router = APIRouter()

@router.post("/simulate", response_model=SimulationResultResponse, status_code=status.HTTP_201_CREATED)
async def run_simulation(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    scenario_in: SimulationScenarioCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Executes a Digital Twin simulation to forecast SOC KPIs based on 'what-if' parameters.
    """
    # 1. Save Scenario
    scenario = SimulationScenario(
        tenant_id=current_user.tenant_id,
        name=scenario_in.name,
        description=scenario_in.description,
        alert_volume_multiplier=scenario_in.alert_volume_multiplier,
        analyst_headcount=scenario_in.analyst_headcount,
        automation_rate=scenario_in.automation_rate
    )
    db.add(scenario)
    await db.commit()
    
    # 2. Run Simulation
    sim_engine = SimulationEngine(db)
    result = await sim_engine.execute_scenario(scenario)
    
    # 3. Generate Optimizations
    opt_engine = OptimizationEngine(db)
    await opt_engine.generate_recommendations(result)
    
    # Refresh to grab relationships
    await db.refresh(result, ["recommendations"])
    
    return result

from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.bas_platform import (
    BasSimulationBase,
    BasSimulationResponse
)

from app.bas_platform.simulation_manager import SimulationManager
from app.bas_platform.validation_engine import ValidationEngine
from app.bas_platform.scoring_engine import ScoringEngine

router = APIRouter()

@router.post("/execute", response_model=BasSimulationResponse, status_code=status.HTTP_201_CREATED)
async def execute_validation_scenario(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    sim_in: BasSimulationBase,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Safely executes a validation scenario, queries security controls for detections, and calculates a readiness score.
    """
    
    # 1. Orchestrate Simulation
    mgr = SimulationManager(db)
    simulation = await mgr.execute_simulation(
        tenant_id=current_user.tenant_id,
        scenario_id=sim_in.scenario_id
    )
    
    # 2. Validate Detections against SIEM/EDR
    val_eng = ValidationEngine(db)
    await val_eng.validate_simulation(simulation.id)
    
    # 3. Calculate Overall Security Readiness Score
    score_eng = ScoringEngine(db)
    simulation = await score_eng.finalize_simulation_score(simulation.id)
    
    return simulation

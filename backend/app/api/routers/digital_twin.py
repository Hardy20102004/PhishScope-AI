from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.digital_twin import (
    TwinAssetNodeResponse, AttackPathGraphResponse,
    SimulationScenarioResponse, ResilienceMetricResponse
)
from app.digital_twin.digital_twin_manager import DigitalTwinManager
from app.digital_twin.attack_path_engine import AttackPathEngine
from app.digital_twin.scenario_simulation_engine import ScenarioSimulationEngine
from app.digital_twin.resilience_assessment_engine import ResilienceAssessmentEngine

router = APIRouter()

@router.get("/assets", response_model=List[TwinAssetNodeResponse])
async def get_assets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manager = DigitalTwinManager(db)
    return await manager.get_assets(current_user.tenant_id)

@router.get("/attack-paths", response_model=List[AttackPathGraphResponse])
async def get_attack_paths(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = AttackPathEngine(db)
    return await engine.get_attack_paths(current_user.tenant_id)

@router.get("/simulations", response_model=List[SimulationScenarioResponse])
async def get_simulations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ScenarioSimulationEngine(db)
    return await engine.get_simulations(current_user.tenant_id)

@router.get("/resilience", response_model=List[ResilienceMetricResponse])
async def get_resilience_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ResilienceAssessmentEngine(db)
    return await engine.get_metrics(current_user.tenant_id)

from typing import Any, List, Dict
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.api import deps
from app.models.user import User
from app.schemas.attack_path import (
    SimulatedAttackPathResponse
)

from app.attack_path.exposure_engine import ExposureEngine
from app.attack_path.blast_radius_engine import BlastRadiusEngine
from app.attack_path.remediation_engine import RemediationPrioritizationEngine

router = APIRouter()

@router.post("/simulate-path", response_model=SimulatedAttackPathResponse)
async def simulate_attack_path(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    source_node_id: uuid.UUID,
    target_node_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Simulates finding a path between a source and a target.
    """
    eng = ExposureEngine(db)
    try:
        path = await eng.simulate_attack_path(current_user.tenant_id, source_node_id, target_node_id)
        return path
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/blast-radius/{node_id}", response_model=List[str])
async def get_blast_radius(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    node_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Returns the downstream blast radius if the given node is compromised.
    """
    eng = BlastRadiusEngine(db)
    impact = await eng.calculate_blast_radius(current_user.tenant_id, node_id)
    return impact

@router.get("/choke-points", response_model=Dict[str, Any])
async def get_choke_points(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Returns prioritized remediation choke points.
    """
    eng = RemediationPrioritizationEngine(db)
    choke_point = await eng.identify_choke_points(current_user.tenant_id)
    return choke_point

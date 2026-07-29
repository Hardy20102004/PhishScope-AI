from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.continuous_validation import CVOptimizationRecommendation
from app.schemas.continuous_validation import (
    SecurityPostureSnapshotResponse,
    SecurityDriftRecordResponse,
    OptimizationRecommendationResponse
)

from app.continuous_validation.posture_engine import SecurityPostureEngine
from app.continuous_validation.drift_engine import SecurityDriftEngine

router = APIRouter()

@router.get("/posture", response_model=SecurityPostureSnapshotResponse)
async def get_security_posture(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Calculates the Apex Security Posture Score.
    """
    mgr = SecurityPostureEngine(db)
    # Simulating the inputs for the MVP
    snapshot = await mgr.calculate_current_posture(current_user.tenant_id, 82.0, 78.0, 60.0)
    return snapshot


@router.get("/drift", response_model=List[SecurityDriftRecordResponse])
async def check_security_drift(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Checks for security drift (regressions) since the last posture snapshot.
    """
    eng = SecurityDriftEngine(db)
    drifts = await eng.check_for_drift(current_user.tenant_id)
    return drifts


@router.get("/optimizations", response_model=List[OptimizationRecommendationResponse])
async def get_optimizations(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the prioritized list of optimizations.
    """
    res = await db.execute(select(CVOptimizationRecommendation).where(CVOptimizationRecommendation.tenant_id == current_user.tenant_id))
    return res.scalars().all()

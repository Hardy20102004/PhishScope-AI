from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.detection_gap import ControlOptimizationPlan
from app.schemas.detection_gap import (
    MitreCoverageMetricResponse,
    DetectionGapRecordResponse,
    ControlOptimizationPlanResponse
)

from app.detection_gap.coverage_engine import CoverageAnalysisEngine
from app.detection_gap.gap_analysis_engine import GapAnalysisEngine

router = APIRouter()

@router.get("/coverage", response_model=float)
async def get_overall_coverage(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Returns the overall enterprise MITRE ATT&CK coverage percentage.
    """
    eng = CoverageAnalysisEngine(db)
    return await eng.get_overall_coverage(current_user.tenant_id)

@router.get("/gaps", response_model=List[DetectionGapRecordResponse])
async def get_detection_gaps(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Runs analysis and returns identified detection gaps.
    """
    eng = GapAnalysisEngine(db)
    return await eng.analyze_gaps(current_user.tenant_id)

@router.get("/optimization-plans", response_model=List[ControlOptimizationPlanResponse])
async def get_optimization_plans(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the prioritized list of detection engineering tasks.
    """
    res = await db.execute(select(ControlOptimizationPlan).where(ControlOptimizationPlan.tenant_id == current_user.tenant_id))
    return res.scalars().all()

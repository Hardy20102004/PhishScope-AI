from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.strategic_defense import StrategicForecast, OptimizationRoadmap, StrategicRecommendation, DecisionApprovalLog
from app.schemas.strategic_defense import (
    StrategicForecastResponse,
    OptimizationRoadmapResponse,
    StrategicRecommendationResponse,
    DecisionApprovalLogResponse
)

from app.strategic_defense.decision_support_engine import DecisionSupportEngine

router = APIRouter()

@router.get("/forecasts", response_model=List[StrategicForecastResponse])
async def get_strategic_forecasts(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves projected risk and operational trends.
    """
    res = await db.execute(select(StrategicForecast).where(StrategicForecast.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/roadmap", response_model=List[OptimizationRoadmapResponse])
async def get_optimization_roadmap(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the multi-year security roadmap.
    """
    res = await db.execute(select(OptimizationRoadmap).where(OptimizationRoadmap.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/recommendations", response_model=List[StrategicRecommendationResponse])
async def get_strategic_recommendations(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves AI-generated strategic recommendations pending human review.
    """
    res = await db.execute(select(StrategicRecommendation).where(StrategicRecommendation.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.post("/recommendations/{rec_id}/approve", response_model=DecisionApprovalLogResponse)
async def approve_recommendation(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    rec_id: uuid.UUID,
    justification: str = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Human approval gate for an AI recommendation.
    """
    dse = DecisionSupportEngine(db)
    log = await dse.record_decision(current_user.tenant_id, rec_id, current_user.id, "APPROVED", justification)
    return log

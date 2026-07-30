from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.cyber_fusion import (
    FusionRecordResponse, CrossDomainRiskScoreResponse,
    StrategicRecommendationResponse
)
from app.cyber_fusion.cyber_fusion_manager import CyberFusionManager
from app.cyber_fusion.executive_analytics_engine import ExecutiveAnalyticsEngine
from app.cyber_fusion.decision_support_engine import DecisionSupportEngine

router = APIRouter()

@router.get("/records", response_model=List[FusionRecordResponse])
async def get_records(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manager = CyberFusionManager(db)
    return await manager.get_fusion_records(current_user.tenant_id)

@router.get("/risk", response_model=List[CrossDomainRiskScoreResponse])
async def get_risk_scores(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ExecutiveAnalyticsEngine(db)
    return await engine.get_risk_scores(current_user.tenant_id)

@router.get("/recommendations", response_model=List[StrategicRecommendationResponse])
async def get_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = DecisionSupportEngine(db)
    return await engine.get_recommendations(current_user.tenant_id)

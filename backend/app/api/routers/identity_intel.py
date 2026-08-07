from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.identity_intel import (
    IdentityTelemetryResponse, BehaviorBaselineResponse,
    AdaptiveTrustScoreResponse, IdentityRiskAnalyticsResponse
)
from app.identity_intel.correlation_engine import CorrelationEngine
from app.identity_intel.behavior_engine import BehaviorEngine
from app.identity_intel.trust_engine import TrustEngine
from app.identity_intel.risk_engine import RiskEngine
from app.identity_intel.executive_intel_engine import ExecutiveIntelEngine

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Telemetry & Behavior
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/telemetry", response_model=List[IdentityTelemetryResponse])
async def get_telemetry(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CorrelationEngine(db)
    return await engine.get_telemetry(current_user.tenant_id)

@router.get("/behavior", response_model=List[BehaviorBaselineResponse])
async def get_behavior_baselines(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = BehaviorEngine(db)
    return await engine.get_baselines(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Trust & Risk
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/trust", response_model=List[AdaptiveTrustScoreResponse])
async def get_trust_scores(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = TrustEngine(db)
    return await engine.get_trust_scores(current_user.tenant_id)

@router.get("/risk", response_model=List[IdentityRiskAnalyticsResponse])
async def get_risk_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = RiskEngine(db)
    return await engine.get_risk_analytics(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Analytics
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_executive_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ExecutiveIntelEngine(db)
    return await engine.get_dashboard_metrics()

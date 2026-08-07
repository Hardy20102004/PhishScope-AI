from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.itdr import (
    ITDRTelemetryEventCreate, ITDRTelemetryEventResponse,
    ITDRBehaviorBaselineResponse, ITDRCredentialAttackResponse,
    ITDRInvestigationCreate, ITDRInvestigationResponse,
    ITDRRiskScoreResponse
)
from app.itdr.telemetry_engine import IdentityTelemetryEngine
from app.itdr.behavior_engine import BehaviorAnalyticsEngine
from app.itdr.credential_attack_engine import CredentialAttackEngine
from app.itdr.investigation_engine import IdentityInvestigationEngine
from app.itdr.risk_engine import IdentityRiskAnalyticsEngine
from app.itdr.executive_analytics import ITDRExecutiveAnalytics

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Telemetry
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/telemetry", response_model=ITDRTelemetryEventResponse)
async def ingest_telemetry(
    event_in: ITDRTelemetryEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = IdentityTelemetryEngine(db)
    return await engine.ingest_telemetry(current_user.tenant_id, event_in.model_dump())

@router.get("/telemetry", response_model=List[ITDRTelemetryEventResponse])
async def get_telemetry(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = IdentityTelemetryEngine(db)
    return await engine.get_recent_telemetry(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Behavior & Attacks
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/baselines", response_model=List[ITDRBehaviorBaselineResponse])
async def get_baselines(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = BehaviorAnalyticsEngine(db)
    return await engine.get_baselines(current_user.tenant_id)

@router.get("/attacks", response_model=List[ITDRCredentialAttackResponse])
async def get_attacks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CredentialAttackEngine(db)
    return await engine.get_attacks(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Investigations
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/investigations", response_model=List[ITDRInvestigationResponse])
async def get_investigations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = IdentityInvestigationEngine(db)
    return await engine.get_investigations(current_user.tenant_id)

@router.post("/investigations", response_model=ITDRInvestigationResponse)
async def create_investigation(
    inv_in: ITDRInvestigationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = IdentityInvestigationEngine(db)
    return await engine.create_investigation(current_user.tenant_id, inv_in.model_dump())

# ─────────────────────────────────────────────────────────────────────────────
# Analytics
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_itdr_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ITDRExecutiveAnalytics(db)
    return await engine.get_dashboard_metrics()

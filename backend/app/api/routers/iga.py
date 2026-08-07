from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.iga import (
    IGALifecycleEventCreate, IGALifecycleEventResponse,
    IGAAccessRequestCreate, IGAAccessRequestResponse,
    IGACertificationCampaignResponse, IGASegregationOfDutiesRuleResponse,
    IGARiskScoreResponse
)
from app.iga.jml_engine import JMLEngine
from app.iga.access_request_engine import AccessRequestEngine
from app.iga.certification_engine import CertificationEngine
from app.iga.sod_engine import SoDEngine
from app.iga.risk_engine import IGARiskEngine
from app.iga.executive_analytics import IGAExecutiveAnalytics

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# JML Lifecycle
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/jml", response_model=IGALifecycleEventResponse)
async def create_jml_event(
    event_in: IGALifecycleEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = JMLEngine(db)
    return await engine.ingest_event(current_user.tenant_id, event_in.model_dump())

@router.get("/jml", response_model=List[IGALifecycleEventResponse])
async def get_jml_events(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = JMLEngine(db)
    return await engine.get_events(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Access Requests
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/access-requests", response_model=List[IGAAccessRequestResponse])
async def get_access_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = AccessRequestEngine(db)
    return await engine.get_requests(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Certifications
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/certifications", response_model=List[IGACertificationCampaignResponse])
async def get_certification_campaigns(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CertificationEngine(db)
    return await engine.get_campaigns(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Segregation of Duties (SoD)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/sod/rules", response_model=List[IGASegregationOfDutiesRuleResponse])
async def get_sod_rules(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = SoDEngine(db)
    return await engine.get_rules(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Analytics
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_iga_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = IGAExecutiveAnalytics(db)
    return await engine.get_dashboard_metrics()

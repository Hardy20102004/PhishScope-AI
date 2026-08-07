from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.authn import (
    AuthnMethodResponse, AuthnEnrollmentResponse,
    AuthnPolicyResponse, AuthnAssuranceLevelResponse, AuthnRiskScoreResponse
)
from app.authn.discovery_engine import DiscoveryEngine
from app.authn.enrollment_engine import EnrollmentEngine
from app.authn.policy_engine import PolicyEngine
from app.authn.assurance_engine import AssuranceEngine
from app.authn.risk_engine import RiskEngine
from app.authn.executive_analytics import ExecutiveAnalytics

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Inventory & Enrollments
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/methods", response_model=List[AuthnMethodResponse])
async def get_methods(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = DiscoveryEngine(db)
    return await engine.get_methods(current_user.tenant_id)

@router.get("/enrollments", response_model=List[AuthnEnrollmentResponse])
async def get_enrollments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = EnrollmentEngine(db)
    return await engine.get_enrollments(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Policies & Assurance
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/policies", response_model=List[AuthnPolicyResponse])
async def get_policies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = PolicyEngine(db)
    return await engine.get_policies(current_user.tenant_id)

@router.get("/assurance", response_model=List[AuthnAssuranceLevelResponse])
async def get_assurance_levels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = AssuranceEngine(db)
    return await engine.get_assurance_levels(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Analytics & Risk
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_authn_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ExecutiveAnalytics(db)
    return await engine.get_dashboard_metrics()

@router.get("/risk", response_model=List[AuthnRiskScoreResponse])
async def get_risk_scores(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = RiskEngine(db)
    return await engine.get_risk_scores(current_user.tenant_id)

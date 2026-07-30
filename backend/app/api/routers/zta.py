from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.zta import (
    ZTAPolicyCreate, ZTAPolicyResponse,
    ZTAContextSnapshotCreate, ZTAContextSnapshotResponse,
    ZTAAccessDecisionResponse, ZTASessionStateResponse
)
from app.zta.policy_engine import ZeroTrustPolicyEngine
from app.zta.context_engine import ContextEvaluationEngine
from app.zta.adaptive_access_engine import AdaptiveAccessEngine
from app.zta.session_engine import SessionIntelligenceEngine
from app.zta.executive_analytics import ZTAExecutiveAnalytics

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Policies
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/policies", response_model=List[ZTAPolicyResponse])
async def get_policies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ZeroTrustPolicyEngine(db)
    policies = await engine.get_policies(current_user.tenant_id)
    return policies

@router.post("/policies", response_model=ZTAPolicyResponse)
async def create_policy(
    policy_in: ZTAPolicyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ZeroTrustPolicyEngine(db)
    policy = await engine.create_policy(current_user.tenant_id, policy_in.model_dump())
    return policy

# ─────────────────────────────────────────────────────────────────────────────
# Verification & Access Evaluation
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/verify-access", response_model=ZTAAccessDecisionResponse)
async def verify_access(
    context_in: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Simulates a continuous verification loop and adaptive access decision.
    """
    # 1. Capture context
    ctx_engine = ContextEvaluationEngine(db)
    snapshot = await ctx_engine.capture_snapshot(current_user.tenant_id, context_in)
    
    # 2. Evaluate access
    access_engine = AdaptiveAccessEngine(db)
    decision = await access_engine.evaluate_access(
        current_user.tenant_id, 
        snapshot.id, 
        context_in, 
        context_in.get("resource_requested", "unknown")
    )
    return decision

# ─────────────────────────────────────────────────────────────────────────────
# Session Intelligence
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/sessions", response_model=List[ZTASessionStateResponse])
async def get_active_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = SessionIntelligenceEngine(db)
    sessions = await engine.get_active_sessions(current_user.tenant_id)
    return sessions

# ─────────────────────────────────────────────────────────────────────────────
# Executive Analytics
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_executive_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ZTAExecutiveAnalytics(db)
    metrics = await engine.get_dashboard_metrics(current_user.tenant_id)
    return metrics

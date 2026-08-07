from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.pam import (
    PAMPrivilegedIdentityResponse,
    PAMJITRequestCreate, PAMJITRequestResponse,
    PAMSessionRecordResponse, PAMCredentialLifecycleResponse,
    PAMPolicyResponse, PAMRiskScoreResponse
)
from app.pam.inventory_engine import PrivilegeInventoryEngine
from app.pam.jit_engine import JITAccessEngine
from app.pam.session_governance_engine import SessionGovernanceEngine
from app.pam.credential_engine import CredentialLifecycleEngine
from app.pam.executive_analytics import PAMExecutiveAnalytics

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Inventory
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/identities", response_model=List[PAMPrivilegedIdentityResponse])
async def get_privileged_identities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = PrivilegeInventoryEngine(db)
    return await engine.get_inventory(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# JIT Workflows
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/jit/requests", response_model=PAMJITRequestResponse)
async def create_jit_request(
    request_in: PAMJITRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = JITAccessEngine(db)
    return await engine.create_request(current_user.tenant_id, request_in.model_dump())

@router.get("/jit/requests", response_model=List[PAMJITRequestResponse])
async def get_jit_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = JITAccessEngine(db)
    return await engine.get_requests(current_user.tenant_id)

@router.post("/jit/requests/{request_id}/approve", response_model=PAMJITRequestResponse)
async def approve_jit_request(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = JITAccessEngine(db)
    req = await engine.approve_request(request_id, current_user.email, "Approved via API")
    if not req:
        raise HTTPException(status_code=404, detail="JIT Request not found")
    return req

# ─────────────────────────────────────────────────────────────────────────────
# Sessions & Credentials
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/sessions", response_model=List[PAMSessionRecordResponse])
async def get_admin_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = SessionGovernanceEngine(db)
    return await engine.get_sessions(current_user.tenant_id)

@router.get("/credentials", response_model=List[PAMCredentialLifecycleResponse])
async def get_credentials(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CredentialLifecycleEngine(db)
    return await engine.get_credentials(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Analytics
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_pam_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = PAMExecutiveAnalytics(db)
    return await engine.get_dashboard_metrics()

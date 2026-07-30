from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.nhi import (
    NHIMachineIdentityResponse, NHICertificateResponse,
    NHITrustRelationshipResponse, NHIRiskScoreResponse
)
from app.nhi.discovery_engine import DiscoveryEngine
from app.nhi.certificate_engine import CertificateEngine
from app.nhi.trust_relationship_engine import TrustRelationshipEngine
from app.nhi.risk_engine import RiskEngine
from app.nhi.executive_analytics import ExecutiveAnalytics

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Inventory
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/identities", response_model=List[NHIMachineIdentityResponse])
async def get_machine_identities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = DiscoveryEngine(db)
    return await engine.get_identities(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Certificates
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/certificates", response_model=List[NHICertificateResponse])
async def get_certificates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CertificateEngine(db)
    return await engine.get_certificates(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Trust Relationships
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/trust", response_model=List[NHITrustRelationshipResponse])
async def get_trust_relationships(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = TrustRelationshipEngine(db)
    return await engine.get_relationships(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Analytics & Risk
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_nhi_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ExecutiveAnalytics(db)
    return await engine.get_dashboard_metrics()

@router.get("/risk", response_model=List[NHIRiskScoreResponse])
async def get_risk_scores(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = RiskEngine(db)
    return await engine.get_risk_scores(current_user.tenant_id)

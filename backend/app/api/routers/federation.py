from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.federation import (
    FederatedProviderResponse, FederationTrustResponse,
    FederationProtocolConfigResponse, FederationCertificateResponse, FederationRiskScoreResponse
)
from app.federation.discovery_engine import DiscoveryEngine
from app.federation.trust_engine import TrustEngine
from app.federation.protocol_engine import ProtocolEngine
from app.federation.metadata_engine import MetadataEngine
from app.federation.risk_engine import RiskEngine
from app.federation.executive_analytics import ExecutiveAnalytics

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Inventory
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/providers", response_model=List[FederatedProviderResponse])
async def get_providers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = DiscoveryEngine(db)
    return await engine.get_providers(current_user.tenant_id)

@router.get("/trusts", response_model=List[FederationTrustResponse])
async def get_trusts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = TrustEngine(db)
    return await engine.get_trusts(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Configs & Metadata
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/protocols", response_model=List[FederationProtocolConfigResponse])
async def get_protocol_configs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ProtocolEngine(db)
    return await engine.get_configs()

@router.get("/certificates", response_model=List[FederationCertificateResponse])
async def get_certificates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = MetadataEngine(db)
    return await engine.get_certificates(current_user.tenant_id)

# ─────────────────────────────────────────────────────────────────────────────
# Analytics & Risk
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/analytics")
async def get_federation_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ExecutiveAnalytics(db)
    return await engine.get_dashboard_metrics()

@router.get("/risk", response_model=List[FederationRiskScoreResponse])
async def get_risk_scores(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = RiskEngine(db)
    return await engine.get_risk_scores(current_user.tenant_id)

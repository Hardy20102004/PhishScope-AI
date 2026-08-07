from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.secrets import SecretMetadata, SecretExposure, SecretPolicy
from app.schemas.secrets import (
    SecretMetadataCreate, SecretMetadataResponse,
    SecretExposureCreate, SecretExposureResponse,
    SecretPolicyCreate, SecretPolicyResponse,
    SecretsExecutiveSummary
)

from app.secrets.secrets_discovery_engine import SecretsDiscoveryEngine
from app.secrets.certificate_governance_engine import CertificateGovernanceEngine
from app.secrets.exposure_assessment_engine import ExposureAssessmentEngine
from app.secrets.policy_engine import PolicyEngine

router = APIRouter()

@router.post("/inventory", response_model=SecretMetadataResponse)
async def register_secret(
    secret_in: SecretMetadataCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecretsDiscoveryEngine(db)
    return await engine.register_secret_metadata(current_user.tenant_id, secret_in)

@router.get("/inventory", response_model=List[SecretMetadataResponse])
async def list_secrets(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecretsDiscoveryEngine(db)
    return await engine.list_secrets(current_user.tenant_id)

@router.get("/certificates", response_model=List[SecretMetadataResponse])
async def list_certificates(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = CertificateGovernanceEngine(db)
    return await engine.list_certificates(current_user.tenant_id)

@router.post("/exposures", response_model=SecretExposureResponse)
async def register_exposure(
    exposure_in: SecretExposureCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ExposureAssessmentEngine(db)
    return await engine.register_exposure(current_user.tenant_id, exposure_in)

@router.get("/exposures", response_model=List[SecretExposureResponse])
async def list_exposures(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ExposureAssessmentEngine(db)
    return await engine.list_exposures(current_user.tenant_id)

@router.post("/policies", response_model=SecretPolicyResponse)
async def register_policy(
    policy_in: SecretPolicyCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = PolicyEngine(db)
    return await engine.register_policy(current_user.tenant_id, policy_in)

@router.get("/executive-summary", response_model=SecretsExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    
    stmt = select(func.count(SecretMetadata.id)).where(SecretMetadata.tenant_id == current_user.tenant_id)
    total_secrets = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(SecretExposure.id)).where(SecretExposure.tenant_id == current_user.tenant_id)
    total_exposures = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    return SecretsExecutiveSummary(
        total_active_secrets=total_secrets,
        total_exposures=total_exposures,
        expiring_certificates_30d=2, # Mock value for frontend representation
        dormant_credentials=5        # Mock value for frontend representation
    )

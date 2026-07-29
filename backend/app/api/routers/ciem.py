from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.ciem import CloudIdentity, CloudEntitlement, IdentityRiskScore, AccessReview
from app.schemas.ciem import (
    CloudIdentityResponse,
    CloudEntitlementResponse,
    IdentityRiskScoreResponse,
    AccessReviewResponse
)

router = APIRouter()

@router.get("/identities", response_model=List[CloudIdentityResponse])
async def get_identities(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all discovered cloud identities.
    """
    res = await db.execute(select(CloudIdentity).where(CloudIdentity.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/identities/{identity_id}/entitlements", response_model=List[CloudEntitlementResponse])
async def get_identity_entitlements(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    identity_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves calculated effective permissions for a specific identity.
    """
    res = await db.execute(select(CloudEntitlement).where(
        CloudEntitlement.tenant_id == current_user.tenant_id,
        CloudEntitlement.identity_id == identity_id
    ))
    return res.scalars().all()

@router.get("/risk", response_model=List[IdentityRiskScoreResponse])
async def get_identity_risk_scores(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves aggregated risk scores for all identities.
    """
    res = await db.execute(select(IdentityRiskScore).where(IdentityRiskScore.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/reviews", response_model=List[AccessReviewResponse])
async def get_access_reviews(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves active access review campaigns for governance.
    """
    res = await db.execute(select(AccessReview).where(AccessReview.tenant_id == current_user.tenant_id))
    return res.scalars().all()

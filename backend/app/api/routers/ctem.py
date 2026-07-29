from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.ctem import (
    AttackSurfaceNode,
    BusinessContextBoundary,
    CloudExposureFinding,
    RemediationPlan
)
from app.schemas.ctem import (
    AttackSurfaceNodeResponse,
    BusinessContextBoundaryResponse,
    CloudExposureFindingResponse,
    RemediationPlanResponse
)

router = APIRouter()

@router.get("/attack-surface", response_model=List[AttackSurfaceNodeResponse])
async def get_attack_surface(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the attack surface inventory for the tenant.
    """
    res = await db.execute(select(AttackSurfaceNode).where(AttackSurfaceNode.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/business-context", response_model=List[BusinessContextBoundaryResponse])
async def get_business_context(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves business context boundaries for the tenant.
    """
    res = await db.execute(select(BusinessContextBoundary).where(BusinessContextBoundary.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/exposures", response_model=List[CloudExposureFindingResponse])
async def get_exposures(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves exposure findings for the tenant, ordered by risk score.
    """
    res = await db.execute(
        select(CloudExposureFinding)
        .where(CloudExposureFinding.tenant_id == current_user.tenant_id)
        .order_by(CloudExposureFinding.contextual_risk_score.desc())
    )
    return res.scalars().all()

@router.get("/remediation-plans", response_model=List[RemediationPlanResponse])
async def get_remediation_plans(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves prioritized AI-generated remediation plans.
    """
    res = await db.execute(select(RemediationPlan).where(RemediationPlan.tenant_id == current_user.tenant_id))
    return res.scalars().all()

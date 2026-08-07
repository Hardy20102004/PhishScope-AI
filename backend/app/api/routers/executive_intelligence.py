from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.executive_intelligence import GovernanceMetric, BusinessImpactIndicator, InvestmentROI, DecisionSupportBrief
from app.schemas.executive_intelligence import (
    GovernanceMetricResponse,
    BusinessImpactIndicatorResponse,
    InvestmentROIResponse,
    DecisionSupportBriefResponse
)

router = APIRouter()

@router.get("/governance", response_model=List[GovernanceMetricResponse])
async def get_governance_metrics(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all compliance and governance metrics.
    """
    res = await db.execute(select(GovernanceMetric).where(GovernanceMetric.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/business-impact", response_model=List[BusinessImpactIndicatorResponse])
async def get_business_impact(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the business impact status of critical services.
    """
    res = await db.execute(select(BusinessImpactIndicator).where(BusinessImpactIndicator.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/investment-roi", response_model=List[InvestmentROIResponse])
async def get_investment_roi(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves ROI and efficiency gains for strategic initiatives.
    """
    res = await db.execute(select(InvestmentROI).where(InvestmentROI.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/briefs", response_model=List[DecisionSupportBriefResponse])
async def get_executive_briefs(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves generated AI decision support briefs for the board.
    """
    res = await db.execute(select(DecisionSupportBrief).where(DecisionSupportBrief.tenant_id == current_user.tenant_id))
    return res.scalars().all()

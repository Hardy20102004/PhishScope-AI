from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.multi_cloud import UnifiedCloudAsset, CrossCloudRelationship, UnifiedRiskScore, ComplianceTrend
from app.schemas.multi_cloud import (
    UnifiedCloudAssetResponse,
    CrossCloudRelationshipResponse,
    UnifiedRiskScoreResponse,
    ComplianceTrendResponse
)

router = APIRouter()

@router.get("/assets", response_model=List[UnifiedCloudAssetResponse])
async def get_unified_assets(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the unified inventory of all cloud assets across all providers.
    """
    res = await db.execute(select(UnifiedCloudAsset).where(UnifiedCloudAsset.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/risk", response_model=UnifiedRiskScoreResponse)
async def get_enterprise_risk_score(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the aggregated Enterprise Cloud Risk Score.
    """
    res = await db.execute(select(UnifiedRiskScore).where(UnifiedRiskScore.tenant_id == current_user.tenant_id))
    score = res.scalars().first()
    if not score:
        raise HTTPException(status_code=404, detail="Risk score not yet calculated")
    return score

@router.get("/compliance", response_model=List[ComplianceTrendResponse])
async def get_compliance_trends(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves compliance trends across frameworks (NIST, CIS, ISO).
    """
    res = await db.execute(select(ComplianceTrend).where(ComplianceTrend.tenant_id == current_user.tenant_id))
    return res.scalars().all()

from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.cspm import CloudAsset, CloudMisconfiguration, ComplianceFinding
from app.schemas.cspm import (
    CloudAssetResponse,
    CloudMisconfigurationResponse,
    ComplianceFindingResponse
)

router = APIRouter()

@router.get("/assets", response_model=List[CloudAssetResponse])
async def get_cloud_assets(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all discovered cloud assets.
    """
    res = await db.execute(select(CloudAsset).where(CloudAsset.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/misconfigurations", response_model=List[CloudMisconfigurationResponse])
async def get_misconfigurations(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves active cloud misconfigurations and vulnerabilities.
    """
    res = await db.execute(select(CloudMisconfiguration).where(CloudMisconfiguration.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/compliance", response_model=List[ComplianceFindingResponse])
async def get_compliance_findings(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves compliance framework assessment results.
    """
    res = await db.execute(select(ComplianceFinding).where(ComplianceFinding.tenant_id == current_user.tenant_id))
    return res.scalars().all()

from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.dspm import CloudDataAsset, DataClassification, DataExposureFinding, DataAccessGovernance
from app.schemas.dspm import (
    CloudDataAssetResponse,
    DataClassificationResponse,
    DataExposureFindingResponse,
    DataAccessGovernanceResponse
)

router = APIRouter()

@router.get("/assets", response_model=List[CloudDataAssetResponse])
async def get_data_assets(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all discovered cloud data assets.
    """
    res = await db.execute(select(CloudDataAsset).where(CloudDataAsset.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/assets/{asset_id}/classification", response_model=List[DataClassificationResponse])
async def get_asset_classifications(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    asset_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves sensitivity classifications for a specific data asset.
    """
    res = await db.execute(select(DataClassification).where(
        DataClassification.tenant_id == current_user.tenant_id,
        DataClassification.asset_id == asset_id
    ))
    return res.scalars().all()

@router.get("/findings", response_model=List[DataExposureFindingResponse])
async def get_exposure_findings(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all exposure and encryption findings across data assets.
    """
    res = await db.execute(select(DataExposureFinding).where(DataExposureFinding.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/assets/{asset_id}/governance", response_model=List[DataAccessGovernanceResponse])
async def get_access_governance(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    asset_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves identities and their access levels for a specific data asset.
    """
    res = await db.execute(select(DataAccessGovernance).where(
        DataAccessGovernance.tenant_id == current_user.tenant_id,
        DataAccessGovernance.asset_id == asset_id
    ))
    return res.scalars().all()

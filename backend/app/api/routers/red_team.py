from typing import Any
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.api import deps
from app.models.user import User
from app.schemas.red_team import (
    RedTeamCampaignBase,
    RedTeamCampaignResponse
)

from app.red_team.campaign_manager import CampaignManager

router = APIRouter()

@router.post("/campaigns", response_model=RedTeamCampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_red_team_campaign(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    camp_in: RedTeamCampaignBase,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Scaffolds a new Red Team campaign and generates the required authorization records for stakeholders to sign.
    """
    
    mgr = CampaignManager(db)
    campaign = await mgr.create_campaign(
        tenant_id=current_user.tenant_id,
        name=camp_in.name,
        description=camp_in.description,
        scope=camp_in.scope_definition
    )
    
    return campaign

@router.post("/campaigns/{campaign_id}/request-authorization", response_model=RedTeamCampaignResponse)
async def request_authorization(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    campaign_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Moves a campaign from DRAFT to PENDING_APPROVAL.
    """
    mgr = CampaignManager(db)
    try:
        campaign = await mgr.request_authorization(campaign_id)
        return campaign
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/campaigns/{campaign_id}/commence", response_model=RedTeamCampaignResponse)
async def commence_campaign(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    campaign_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Enforces governance gates. Only allows a campaign to start if all stakeholders have signed.
    """
    mgr = CampaignManager(db)
    try:
        campaign = await mgr.commence_campaign(campaign_id)
        return campaign
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.cdr import CloudDetection, CDRCloudInvestigation, CloudTelemetryEvent, ResponseAction
from app.schemas.cdr import (
    CloudDetectionResponse,
    CloudInvestigationResponse,
    CloudTelemetryEventResponse,
    ResponseActionResponse
)

router = APIRouter()

@router.get("/detections", response_model=List[CloudDetectionResponse])
async def get_active_detections(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all active cloud detections.
    """
    res = await db.execute(select(CloudDetection).where(CloudDetection.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/investigations", response_model=List[CloudInvestigationResponse])
async def get_investigations(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves correlated cloud investigation containers.
    """
    res = await db.execute(select(CDRCloudInvestigation).where(CDRCloudInvestigation.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/telemetry", response_model=List[CloudTelemetryEventResponse])
async def get_telemetry_stream(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves normalized raw cloud telemetry (for timeline exploration).
    """
    res = await db.execute(select(CloudTelemetryEvent).where(
        CloudTelemetryEvent.tenant_id == current_user.tenant_id
    ).order_by(CloudTelemetryEvent.timestamp.desc()).limit(100))
    return res.scalars().all()

@router.get("/investigations/{investigation_id}/actions", response_model=List[ResponseActionResponse])
async def get_response_actions(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    investigation_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves proposed response actions for an investigation.
    """
    res = await db.execute(select(ResponseAction).where(
        ResponseAction.tenant_id == current_user.tenant_id,
        ResponseAction.investigation_id == investigation_id
    ))
    return res.scalars().all()

from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.cwpp import CloudWorkload, RuntimeEvent, BehaviorAnomaly, WorkloadRiskScore
from app.schemas.cwpp import (
    CloudWorkloadResponse,
    RuntimeEventResponse,
    BehaviorAnomalyResponse,
    WorkloadRiskScoreResponse
)

router = APIRouter()

@router.get("/workloads", response_model=List[CloudWorkloadResponse])
async def get_cloud_workloads(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all discovered cloud workloads (VMs, Containers, Serverless).
    """
    res = await db.execute(select(CloudWorkload).where(CloudWorkload.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/workloads/{workload_id}/events", response_model=List[RuntimeEventResponse])
async def get_runtime_events(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    workload_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves raw runtime events for a specific workload.
    """
    res = await db.execute(select(RuntimeEvent).where(
        RuntimeEvent.tenant_id == current_user.tenant_id,
        RuntimeEvent.workload_id == workload_id
    ).order_by(RuntimeEvent.timestamp.desc()).limit(100))
    return res.scalars().all()

@router.get("/anomalies", response_model=List[BehaviorAnomalyResponse])
async def get_behavioral_anomalies(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves identified behavioral deviations across all workloads.
    """
    res = await db.execute(select(BehaviorAnomaly).where(BehaviorAnomaly.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/risk", response_model=List[WorkloadRiskScoreResponse])
async def get_workload_risk_scores(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves aggregated risk scores for workloads.
    """
    res = await db.execute(select(WorkloadRiskScore).where(WorkloadRiskScore.tenant_id == current_user.tenant_id))
    return res.scalars().all()

from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.command_center import (
    EnterpriseCloudMetric,
    OperationalMetric,
    CommandCenterAuditLog
)
from app.schemas.command_center import (
    EnterpriseCloudMetricResponse,
    OperationalMetricResponse,
    CommandCenterAuditLogResponse,
    CommandCenterAuditLogBase
)

router = APIRouter()

@router.get("/health", response_model=List[EnterpriseCloudMetricResponse])
async def get_enterprise_health(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the aggregated enterprise cloud health metrics.
    """
    res = await db.execute(select(EnterpriseCloudMetric).where(EnterpriseCloudMetric.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/operations", response_model=List[OperationalMetricResponse])
async def get_operational_metrics(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves SOC and cloud defense operational metrics.
    """
    res = await db.execute(select(OperationalMetric).where(OperationalMetric.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/audit", response_model=List[CommandCenterAuditLogResponse])
async def get_audit_logs(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the human approval and override audit logs.
    """
    res = await db.execute(select(CommandCenterAuditLog).where(CommandCenterAuditLog.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.post("/approvals", response_model=CommandCenterAuditLogResponse, status_code=status.HTTP_201_CREATED)
async def create_approval(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    approval_in: CommandCenterAuditLogBase,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Records a human approval gate decision.
    """
    log_entry = CommandCenterAuditLog(
        tenant_id=current_user.tenant_id,
        action_type=approval_in.action_type,
        target_resource=approval_in.target_resource,
        actor_id=current_user.id,
        justification=approval_in.justification
    )
    db.add(log_entry)
    await db.commit()
    await db.refresh(log_entry)
    return log_entry

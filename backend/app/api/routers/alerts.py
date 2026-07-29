import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.alert_management import Alert, AlertCorrelationGroup
from app.schemas.alert_management import (
    AlertCreate, 
    AlertUpdate, 
    AlertResponse, 
    AlertCorrelationGroupResponse,
    AlertAnalyticsDashboardResponse,
    AlertLifecycleEventResponse,
    AlertAssignmentResponse
)
from app.alert_management.ingestion import AlertIngestionEngine
from app.alert_management.lifecycle import AlertLifecycleManager

router = APIRouter()

@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def ingest_alert(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    alert_in: AlertCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Ingest a new security alert from an external system.
    """
    ingestion_engine = AlertIngestionEngine(db)
    alert = await ingestion_engine.ingest_webhook(
        raw_payload=alert_in.model_dump(exclude_unset=True),
        source=alert_in.source,
        tenant_id=alert_in.tenant_id,
        background_tasks=background_tasks
    )
    return alert

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    db: AsyncSession = Depends(deps.get_async_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve active security alerts for the current tenant.
    """
    result = await db.execute(
        select(Alert)
        .where(Alert.tenant_id == current_user.tenant_id)
        .order_by(Alert.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    alerts = result.scalars().all()
    return alerts

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get details of a specific alert by ID.
    """
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id, Alert.tenant_id == current_user.tenant_id)
    )
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.patch("/{alert_id}/status", response_model=AlertResponse)
async def update_alert_status(
    alert_id: uuid.UUID,
    status_update: AlertUpdate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update the lifecycle status of an alert.
    """
    lifecycle_manager = AlertLifecycleManager(db)
    
    if not status_update.status:
         raise HTTPException(status_code=400, detail="Must provide new status")
         
    try:
        alert = await lifecycle_manager.update_status(
            alert_id=alert_id,
            new_status=status_update.status,
            user_id=current_user.id,
            comment=status_update.resolution_reason
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    return alert

@router.get("/correlations/{group_id}", response_model=AlertCorrelationGroupResponse)
async def get_correlation_group(
    group_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a correlation group and all its associated alerts.
    """
    result = await db.execute(
        select(AlertCorrelationGroup).where(
            AlertCorrelationGroup.id == group_id, 
            AlertCorrelationGroup.tenant_id == current_user.tenant_id
        )
    )
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Correlation Group not found")
    return group

@router.get("/dashboard/analytics", response_model=AlertAnalyticsDashboardResponse)
async def get_analytics(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get SOC Dashboard high-level analytics metrics.
    """
    from app.alert_management.analytics import AlertAnalyticsEngine
    analytics_engine = AlertAnalyticsEngine(db)
    return await analytics_engine.get_dashboard_metrics(current_user.tenant_id)

@router.get("/{alert_id}/audit", response_model=List[AlertLifecycleEventResponse])
async def get_alert_audit_trail(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the chronological lifecycle audit trail of an alert.
    """
    from app.alert_management.audit import AlertAuditService
    audit_service = AlertAuditService(db)
    
    # Optional: Check if alert belongs to tenant
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.tenant_id == current_user.tenant_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Alert not found")
        
    return await audit_service.get_audit_trail(alert_id)

@router.post("/{alert_id}/assign", response_model=AlertAssignmentResponse)
async def assign_alert(
    alert_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Assign an alert to an analyst.
    """
    from app.alert_management.assignment import AlertAssignmentEngine
    assignment_engine = AlertAssignmentEngine(db)
    
    # Check if alert belongs to tenant
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.tenant_id == current_user.tenant_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Alert not found")
        
    assignment = await assignment_engine.assign_alert(
        alert_id=alert_id,
        user_id=user_id,
        assigned_by=current_user.id
    )
    return assignment


from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.api import deps
from app.schemas.cyber_command import (
    CyberCommandOverview, StrategicPlanCreate, StrategicPlanResponse,
    StrategicPlanListResponse, EnterpriseHealthMetricResponse, EnterpriseHealthMetricListResponse
)
from app.services.cyber_command.manager import CyberCommandManager

router = APIRouter()

@router.get("/overview", response_model=CyberCommandOverview)
def get_command_overview(db: Session = Depends(deps.get_db)) -> Any:
    """Get high-level overview of the Cyber Command Platform."""
    manager = CyberCommandManager(db)
    stats = manager.get_overview_stats()
    
    return CyberCommandOverview(
        global_health_score=stats["global_health_score"],
        active_operations_count=stats["active_operations_count"],
        critical_alerts=stats["critical_alerts"],
        strategic_alignment_score=stats["strategic_alignment_score"],
        ai_strategic_briefing=stats["ai_strategic_briefing"]
    )

@router.post("/strategy/plans", response_model=StrategicPlanResponse)
def create_strategic_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_in: StrategicPlanCreate
) -> Any:
    """Create a new strategic cyber plan."""
    manager = CyberCommandManager(db)
    plan = manager.decision.create_plan(plan_in)
    return {
        "status": "success",
        "data": plan,
        "meta": {"request_id": "req-cmd-1", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/strategy/plans", response_model=StrategicPlanListResponse)
def get_strategic_plans(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get all strategic plans."""
    manager = CyberCommandManager(db)
    plans = manager.decision.get_plans(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": plans,
        "meta": {"request_id": "req-cmd-2", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/health", response_model=EnterpriseHealthMetricListResponse)
def get_enterprise_health(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get enterprise health metrics across all domains."""
    manager = CyberCommandManager(db)
    metrics = manager.kpi.get_metrics(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": metrics,
        "meta": {"request_id": "req-cmd-3", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

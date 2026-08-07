from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.schemas.appsec_command_center import (
    AppSecExecutiveMetricCreate, AppSecExecutiveMetricResponse,
    EngineeringProductivityMetricCreate, EngineeringProductivityMetricResponse,
    AppSecConsolidatedFindingCreate, AppSecConsolidatedFindingResponse,
    AppSecGovernanceDecisionCreate, AppSecGovernanceDecisionResponse
)

from app.appsec_command_center.appsec_command_center_manager import AppSecCommandCenterManager
from app.appsec_command_center.devsecops_intelligence_engine import DevSecOpsIntelligenceEngine
from app.appsec_command_center.executive_decision_support_engine import ExecutiveDecisionSupportEngine

router = APIRouter()

@router.post("/consolidated-findings", response_model=AppSecConsolidatedFindingResponse)
async def ingest_finding(
    finding_in: AppSecConsolidatedFindingCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = AppSecCommandCenterManager(db)
    return await engine.ingest_finding(current_user.tenant_id, finding_in)

@router.get("/consolidated-findings", response_model=List[AppSecConsolidatedFindingResponse])
async def list_findings(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = AppSecCommandCenterManager(db)
    return await engine.list_findings(current_user.tenant_id)

@router.post("/engineering-intelligence", response_model=EngineeringProductivityMetricResponse)
async def log_engineering_metric(
    metric_in: EngineeringProductivityMetricCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DevSecOpsIntelligenceEngine(db)
    return await engine.log_metric(current_user.tenant_id, metric_in)

@router.get("/engineering-intelligence", response_model=List[EngineeringProductivityMetricResponse])
async def get_engineering_metrics(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DevSecOpsIntelligenceEngine(db)
    return await engine.get_metrics(current_user.tenant_id)

@router.post("/executive-summary", response_model=AppSecExecutiveMetricResponse)
async def log_executive_metric(
    metric_in: AppSecExecutiveMetricCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ExecutiveDecisionSupportEngine(db)
    return await engine.log_executive_metric(current_user.tenant_id, metric_in)

@router.get("/executive-summary", response_model=List[AppSecExecutiveMetricResponse])
async def get_executive_metrics(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ExecutiveDecisionSupportEngine(db)
    return await engine.get_executive_metrics(current_user.tenant_id)

@router.post("/governance", response_model=AppSecGovernanceDecisionResponse)
async def propose_decision(
    decision_in: AppSecGovernanceDecisionCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ExecutiveDecisionSupportEngine(db)
    return await engine.propose_governance_decision(current_user.tenant_id, current_user.id, decision_in)

@router.post("/governance/{decision_id}/approve", response_model=AppSecGovernanceDecisionResponse)
async def approve_decision(
    decision_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ExecutiveDecisionSupportEngine(db)
    return await engine.approve_governance_decision(current_user.tenant_id, decision_id, current_user.id)

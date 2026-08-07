from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.devsecops import PipelineRun, SecurityGate, GateStatus, SDLCWorkflow
from app.schemas.devsecops import (
    PipelineRunCreate, PipelineRunResponse,
    SecurityGateCreate, SecurityGateResponse,
    DeveloperMetricCreate, DeveloperMetricResponse,
    DevSecOpsExecutiveSummary, SDLCWorkflowCreate, SDLCWorkflowResponse
)
from app.devsecops.pipeline_engine import PipelineIntegrationEngine
from app.devsecops.security_gate_engine import SecurityGateEngine
from app.devsecops.developer_experience_engine import DeveloperExperienceEngine

router = APIRouter()

@router.post("/pipelines", response_model=PipelineRunResponse)
async def create_pipeline_run(
    run_in: PipelineRunCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = PipelineIntegrationEngine(db)
    return await engine.register_pipeline_run(current_user.tenant_id, run_in)

@router.get("/pipelines", response_model=List[PipelineRunResponse])
async def list_pipeline_runs(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = PipelineIntegrationEngine(db)
    return await engine.list_pipeline_runs(current_user.tenant_id)

@router.post("/gates", response_model=SecurityGateResponse)
async def record_security_gate(
    gate_in: SecurityGateCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecurityGateEngine(db)
    return await engine.record_gate_result(current_user.tenant_id, gate_in)

@router.get("/gates/{pipeline_run_id}", response_model=List[SecurityGateResponse])
async def get_gates_for_pipeline(
    pipeline_run_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecurityGateEngine(db)
    return await engine.get_gates_for_pipeline(pipeline_run_id)

@router.post("/developer-metrics", response_model=DeveloperMetricResponse)
async def update_developer_metric(
    metric_in: DeveloperMetricCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DeveloperExperienceEngine(db)
    return await engine.update_developer_metric(current_user.tenant_id, metric_in)

@router.get("/developer-metrics", response_model=List[DeveloperMetricResponse])
async def list_top_developers(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DeveloperExperienceEngine(db)
    return await engine.list_top_developers(current_user.tenant_id)

@router.get("/executive-summary", response_model=DevSecOpsExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    
    # Total pipelines
    stmt = select(func.count(PipelineRun.id)).where(PipelineRun.tenant_id == current_user.tenant_id)
    total_pipelines = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    # Failed gates
    stmt = select(func.count(SecurityGate.id)).where(
        SecurityGate.tenant_id == current_user.tenant_id,
        SecurityGate.status == GateStatus.FAIL
    )
    failed_gates = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    # Exceptions
    stmt = select(func.count(SDLCWorkflow.id)).where(
        SDLCWorkflow.tenant_id == current_user.tenant_id,
        SDLCWorkflow.status == "PENDING"
    )
    open_exceptions = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    return DevSecOpsExecutiveSummary(
        total_pipelines_run=total_pipelines,
        failed_security_gates=failed_gates,
        open_exception_requests=open_exceptions,
        average_security_score=85.0 # Placeholder
    )

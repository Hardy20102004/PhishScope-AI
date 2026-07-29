from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.iac import IaCTemplate, IaCConfigurationFinding, IaCDeploymentGovernance
from app.schemas.iac import (
    IaCTemplateCreate, IaCTemplateResponse,
    IaCConfigurationFindingCreate, IaCConfigurationFindingResponse,
    IaCDeploymentGovernanceCreate, IaCDeploymentGovernanceResponse,
    IaCExecutiveSummary
)

from app.iac.iac_discovery_engine import IaCDiscoveryEngine
from app.iac.template_analysis_engine import TemplateAnalysisEngine
from app.iac.deployment_governance_engine import DeploymentGovernanceEngine

router = APIRouter()

@router.post("/templates", response_model=IaCTemplateResponse)
async def register_template(
    template_in: IaCTemplateCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = IaCDiscoveryEngine(db)
    return await engine.register_template(current_user.tenant_id, template_in)

@router.get("/templates", response_model=List[IaCTemplateResponse])
async def list_templates(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = IaCDiscoveryEngine(db)
    return await engine.list_templates(current_user.tenant_id)

@router.post("/findings", response_model=IaCConfigurationFindingResponse)
async def register_finding(
    finding_in: IaCConfigurationFindingCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = TemplateAnalysisEngine(db)
    return await engine.register_finding(current_user.tenant_id, finding_in)

@router.get("/findings", response_model=List[IaCConfigurationFindingResponse])
async def list_findings(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = TemplateAnalysisEngine(db)
    return await engine.list_findings(current_user.tenant_id)

@router.post("/deployments", response_model=IaCDeploymentGovernanceResponse)
async def register_deployment(
    deployment_in: IaCDeploymentGovernanceCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DeploymentGovernanceEngine(db)
    return await engine.request_deployment(current_user.tenant_id, deployment_in)

@router.post("/deployments/{deployment_id}/approve", response_model=IaCDeploymentGovernanceResponse)
async def approve_deployment(
    deployment_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DeploymentGovernanceEngine(db)
    deployment = await engine.approve_deployment(current_user.tenant_id, deployment_id, current_user.id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment

@router.get("/executive-summary", response_model=IaCExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    
    stmt = select(func.count(IaCTemplate.id)).where(IaCTemplate.tenant_id == current_user.tenant_id)
    total_templates = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(IaCConfigurationFinding.id)).where(
        IaCConfigurationFinding.tenant_id == current_user.tenant_id,
        IaCConfigurationFinding.severity == "CRITICAL"
    )
    critical_findings = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    return IaCExecutiveSummary(
        total_templates=total_templates,
        critical_findings=critical_findings,
        pending_deployments=3, # Mock value
        blocked_deployments=1  # Mock value
    )

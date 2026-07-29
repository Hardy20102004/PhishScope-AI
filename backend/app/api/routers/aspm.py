from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.aspm import (
    EnterpriseApplicationCreate, EnterpriseApplicationResponse,
    CodeRepositoryCreate, CodeRepositoryResponse,
    SecurityFindingCreate, SecurityFindingResponse,
    ApplicationRiskResponse, ASPMExecutiveSummary
)
from app.aspm.inventory_engine import ApplicationInventoryEngine
from app.aspm.repository_engine import RepositoryIntegrationEngine
from app.aspm.posture_engine import PostureAnalyticsEngine
from app.aspm.risk_engine import ApplicationRiskEngine

router = APIRouter()

@router.post("/applications", response_model=EnterpriseApplicationResponse)
async def create_application(
    app_in: EnterpriseApplicationCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ApplicationInventoryEngine(db)
    return await engine.register_application(current_user.tenant_id, app_in)

@router.get("/applications", response_model=List[EnterpriseApplicationResponse])
async def list_applications(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ApplicationInventoryEngine(db)
    return await engine.list_applications(current_user.tenant_id)

@router.post("/repositories", response_model=CodeRepositoryResponse)
async def create_repository(
    repo_in: CodeRepositoryCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = RepositoryIntegrationEngine(db)
    return await engine.register_repository(current_user.tenant_id, repo_in)

@router.get("/repositories", response_model=List[CodeRepositoryResponse])
async def list_repositories(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = RepositoryIntegrationEngine(db)
    return await engine.list_repositories(current_user.tenant_id)

@router.post("/findings", response_model=SecurityFindingResponse)
async def create_finding(
    finding_in: SecurityFindingCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = PostureAnalyticsEngine(db)
    return await engine.ingest_finding(current_user.tenant_id, finding_in)

@router.get("/applications/{app_id}/risk", response_model=ApplicationRiskResponse)
async def calculate_application_risk(
    app_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ApplicationRiskEngine(db)
    return await engine.calculate_risk(app_id)

@router.get("/executive-summary", response_model=ASPMExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Aggregating manually for prototype
    inv_engine = ApplicationInventoryEngine(db)
    apps = await inv_engine.list_applications(current_user.tenant_id)
    
    repo_engine = RepositoryIntegrationEngine(db)
    repos = await repo_engine.list_repositories(current_user.tenant_id)
    
    posture_engine = PostureAnalyticsEngine(db)
    posture = await posture_engine.get_posture_summary(current_user.tenant_id)
    
    return ASPMExecutiveSummary(
        total_applications=len(apps),
        critical_applications=sum(1 for a in apps if a.criticality.value == "CRITICAL"),
        total_repositories=len(repos),
        average_risk_score=0.0, # Placeholder
        open_critical_findings=posture.get("critical", 0),
        open_high_findings=posture.get("high", 0)
    )

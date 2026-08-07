from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.dast import DASTScan, DASTTarget, DASTFinding, DASTScanStatus, DASTFindingSeverity
from app.schemas.dast import (
    DASTTargetCreate, DASTTargetResponse,
    DASTScanCreate, DASTScanResponse,
    DASTFindingCreate, DASTFindingResponse,
    DASTGuidanceCreate, DASTGuidanceResponse,
    DASTExecutiveSummary
)

from app.dast.application_discovery_engine import ApplicationDiscoveryEngine
from app.dast.runtime_assessment_engine import RuntimeAssessmentEngine
from app.dast.security_finding_engine import SecurityFindingEngine

router = APIRouter()

@router.post("/targets", response_model=DASTTargetResponse)
async def register_target(
    target_in: DASTTargetCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ApplicationDiscoveryEngine(db)
    return await engine.register_target(current_user.tenant_id, target_in)

@router.get("/targets", response_model=List[DASTTargetResponse])
async def list_targets(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ApplicationDiscoveryEngine(db)
    return await engine.list_targets(current_user.tenant_id)

@router.post("/scans", response_model=DASTScanResponse)
async def initiate_scan(
    scan_in: DASTScanCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = RuntimeAssessmentEngine(db)
    return await engine.initiate_scan(current_user.tenant_id, scan_in)

@router.get("/scans", response_model=List[DASTScanResponse])
async def list_scans(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = RuntimeAssessmentEngine(db)
    return await engine.list_scans(current_user.tenant_id)

@router.post("/findings", response_model=DASTFindingResponse)
async def add_finding(
    finding_in: DASTFindingCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecurityFindingEngine(db)
    return await engine.add_finding(current_user.tenant_id, finding_in)

@router.get("/findings", response_model=List[DASTFindingResponse])
async def list_findings(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecurityFindingEngine(db)
    return await engine.list_findings(current_user.tenant_id)

@router.get("/executive-summary", response_model=DASTExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    
    stmt = select(func.count(DASTTarget.id)).where(DASTTarget.tenant_id == current_user.tenant_id)
    total_targets = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(DASTScan.id)).where(
        DASTScan.tenant_id == current_user.tenant_id,
        DASTScan.status == DASTScanStatus.RUNNING
    )
    active_scans = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(DASTFinding.id)).where(
        DASTFinding.tenant_id == current_user.tenant_id,
        DASTFinding.severity == DASTFindingSeverity.CRITICAL
    )
    critical_findings = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(DASTFinding.id)).where(
        DASTFinding.tenant_id == current_user.tenant_id,
        DASTFinding.severity == DASTFindingSeverity.HIGH
    )
    high_findings = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    return DASTExecutiveSummary(
        total_targets=total_targets,
        active_scans=active_scans,
        critical_findings=critical_findings,
        high_findings=high_findings,
        endpoints_assessed_30d=1542 # Placeholder for analytics
    )

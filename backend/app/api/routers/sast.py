from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.sast import SASTScan, SASTFinding, FindingSeverity
from app.schemas.sast import (
    SASTScanCreate, SASTScanResponse,
    SASTFindingCreate, SASTFindingResponse,
    SASTRuleCreate, SASTRuleResponse,
    SASTGuidanceCreate, SASTGuidanceResponse,
    SASTExecutiveSummary
)

from app.sast.source_analysis_engine import SourceAnalysisEngine
from app.sast.rule_evaluation_engine import RuleEvaluationEngine
from app.sast.security_finding_engine import SecurityFindingEngine
from app.sast.secure_coding_guidance_engine import SecureCodingGuidanceEngine

router = APIRouter()

@router.post("/scans", response_model=SASTScanResponse)
async def initiate_scan(
    scan_in: SASTScanCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SourceAnalysisEngine(db)
    return await engine.initiate_scan(current_user.tenant_id, scan_in)

@router.get("/scans", response_model=List[SASTScanResponse])
async def list_scans(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SourceAnalysisEngine(db)
    return await engine.list_scans(current_user.tenant_id)

@router.post("/findings", response_model=SASTFindingResponse)
async def add_finding(
    finding_in: SASTFindingCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecurityFindingEngine(db)
    return await engine.add_finding(current_user.tenant_id, finding_in)

@router.get("/findings", response_model=List[SASTFindingResponse])
async def list_findings(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecurityFindingEngine(db)
    return await engine.list_findings(current_user.tenant_id)

@router.post("/rules", response_model=SASTRuleResponse)
async def register_rule(
    rule_in: SASTRuleCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = RuleEvaluationEngine(db)
    return await engine.register_rule(current_user.tenant_id, rule_in)

@router.get("/rules", response_model=List[SASTRuleResponse])
async def list_rules(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = RuleEvaluationEngine(db)
    return await engine.list_rules(current_user.tenant_id)

@router.post("/guidance/generate", response_model=SASTGuidanceResponse)
async def generate_guidance(
    guidance_in: SASTGuidanceCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SecureCodingGuidanceEngine(db)
    return await engine.generate_guidance(current_user.tenant_id, guidance_in)

@router.get("/executive-summary", response_model=SASTExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    
    stmt = select(func.count(SASTScan.id)).where(SASTScan.tenant_id == current_user.tenant_id)
    total_scans = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(SASTFinding.id)).where(
        SASTFinding.tenant_id == current_user.tenant_id,
        SASTFinding.severity == FindingSeverity.CRITICAL
    )
    critical = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(SASTFinding.id)).where(
        SASTFinding.tenant_id == current_user.tenant_id,
        SASTFinding.severity == FindingSeverity.HIGH
    )
    high = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    return SASTExecutiveSummary(
        total_scans=total_scans,
        critical_findings=critical,
        high_findings=high,
        average_lines_scanned=24000 # Placeholder
    )

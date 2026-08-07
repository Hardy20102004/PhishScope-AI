from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.reporting_engine import (
    ForensicReportCreate,
    ForensicReportResponse
)

from app.reporting_engine.report_manager import ReportManager
from app.reporting_engine.generation_engine import GenerationEngine

router = APIRouter()

@router.post("/reports", response_model=ForensicReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_forensic_report(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    report_in: ForensicReportCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Scaffolds a new forensic report, compiles sections, and digitally signs it for court readiness.
    """
    # 1. Initialize Report & Scaffold Sections
    mgr = ReportManager(db)
    report = await mgr.initialize_report(
        tenant_id=current_user.tenant_id,
        title=report_in.title,
        report_type=report_in.report_type,
        author_id=current_user.email,
        inv_id=report_in.investigation_id
    )
    
    # 2. Finalize & Sign (in a real scenario, this would be a separate endpoint after editing)
    gen = GenerationEngine(db)
    await gen.finalize_report(report.id)
        
    await db.refresh(report, ["sections"])
    return report

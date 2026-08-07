from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.api import deps
from app.schemas.cyber_governance import (
    CyberGovernanceOverview, GovernancePolicyCreate, GovernancePolicyResponse,
    GovernancePolicyListResponse, BoardReportSummaryResponse, BoardReportSummaryListResponse
)
from app.services.cyber_governance.manager import CyberGovernanceManager

router = APIRouter()

@router.get("/overview", response_model=CyberGovernanceOverview)
def get_governance_overview(db: Session = Depends(deps.get_db)) -> Any:
    """Get high-level overview of the Cyber Governance Platform."""
    manager = CyberGovernanceManager(db)
    stats = manager.get_overview_stats()
    
    return CyberGovernanceOverview(
        overall_maturity_score=stats["overall_maturity_score"],
        active_policies_count=stats["active_policies_count"],
        critical_risks_count=stats["critical_risks_count"],
        board_reports_generated=stats["board_reports_generated"],
        ai_recommendations=[
            "Update ISO 27001 Access Control policy to align with Zero Trust initiative.",
            "Review Q3 Board Report draft for Risk Committee."
        ]
    )

@router.post("/policies", response_model=GovernancePolicyResponse)
def create_governance_policy(
    *,
    db: Session = Depends(deps.get_db),
    policy_in: GovernancePolicyCreate
) -> Any:
    """Create a new governance policy."""
    manager = CyberGovernanceManager(db)
    policy = manager.policy.create_policy(policy_in)
    return {
        "status": "success",
        "data": policy,
        "meta": {"request_id": "req-gov-1", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/policies", response_model=GovernancePolicyListResponse)
def get_governance_policies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get all governance policies."""
    manager = CyberGovernanceManager(db)
    policies = manager.policy.get_policies(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": policies,
        "meta": {"request_id": "req-gov-2", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/board-reports", response_model=BoardReportSummaryListResponse)
def get_board_reports(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get all board reports."""
    manager = CyberGovernanceManager(db)
    reports = manager.board.get_reports(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": reports,
        "meta": {"request_id": "req-gov-3", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.base import APIResponse
from app.models.cyber_governance import GovernanceStatus, PolicyStatus

class CyberGovernanceKPIBase(BaseModel):
    metric_name: str
    metric_value: float
    target_value: float
    category: str

class CyberGovernanceKPICreate(CyberGovernanceKPIBase):
    pass

class CyberGovernanceKPI(CyberGovernanceKPIBase):
    id: UUID
    evaluated_at: datetime

    class Config:
        orm_mode = True

class GovernancePolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    version: str = "1.0"
    framework: str

class GovernancePolicyCreate(GovernancePolicyBase):
    pass

class GovernancePolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    framework: Optional[str] = None
    status: Optional[PolicyStatus] = None
    next_review_date: Optional[datetime] = None

class GovernancePolicy(GovernancePolicyBase):
    id: UUID
    status: PolicyStatus
    created_at: datetime
    updated_at: datetime
    next_review_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class RiskOversightMetricBase(BaseModel):
    risk_domain: str
    risk_score: float
    confidence_level: float
    details: Dict[str, Any] = Field(default_factory=dict)

class RiskOversightMetricCreate(RiskOversightMetricBase):
    pass

class RiskOversightMetric(RiskOversightMetricBase):
    id: UUID
    evaluated_at: datetime

    class Config:
        orm_mode = True

class BoardReportSummaryBase(BaseModel):
    title: str
    quarter: str
    summary_text: str
    investment_summary: Dict[str, Any] = Field(default_factory=dict)
    risk_summary: Dict[str, Any] = Field(default_factory=dict)

class BoardReportSummaryCreate(BoardReportSummaryBase):
    generated_by_ai: bool = True

class BoardReportSummary(BoardReportSummaryBase):
    id: UUID
    generated_by_ai: bool
    created_at: datetime

    class Config:
        orm_mode = True

class CyberGovernanceOverview(BaseModel):
    overall_maturity_score: float
    active_policies_count: int
    critical_risks_count: int
    board_reports_generated: int
    ai_recommendations: List[str]

class CyberGovernanceKPIResponse(APIResponse[CyberGovernanceKPI]):
    pass

class CyberGovernanceKPIListResponse(APIResponse[List[CyberGovernanceKPI]]):
    pass

class GovernancePolicyResponse(APIResponse[GovernancePolicy]):
    pass

class GovernancePolicyListResponse(APIResponse[List[GovernancePolicy]]):
    pass

class RiskOversightMetricResponse(APIResponse[RiskOversightMetric]):
    pass

class RiskOversightMetricListResponse(APIResponse[List[RiskOversightMetric]]):
    pass

class BoardReportSummaryResponse(APIResponse[BoardReportSummary]):
    pass

class BoardReportSummaryListResponse(APIResponse[List[BoardReportSummary]]):
    pass

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.predictive_risk import (
    ForecastInterval, PlanStatus, ApprovalGate
)

# ─────────────────────────────────────────────────────────────────────────────
# Forecasts
# ─────────────────────────────────────────────────────────────────────────────
class RiskForecastBase(BaseModel):
    domain: str
    interval: ForecastInterval
    current_risk_score: float
    projected_risk_score: float
    confidence_interval: float
    underlying_assumptions: List[Dict[str, Any]] = Field(default_factory=list)

class RiskForecastResponse(RiskForecastBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    generated_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Strategic Plans
# ─────────────────────────────────────────────────────────────────────────────
class StrategicPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_maturity_level: int
    status: PlanStatus
    milestones: List[Dict[str, Any]] = Field(default_factory=list)

class StrategicPlanResponse(StrategicPlanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Investments
# ─────────────────────────────────────────────────────────────────────────────
class InvestmentScenarioBase(BaseModel):
    name: str
    budget_estimate_usd: float
    forecasted_risk_reduction: float
    resource_allocations: Dict[str, Any] = Field(default_factory=dict)

class InvestmentScenarioResponse(InvestmentScenarioBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    analyzed_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Governance Decisions
# ─────────────────────────────────────────────────────────────────────────────
class ExecutiveDecisionBase(BaseModel):
    reference_id: str
    reference_type: str
    decision: ApprovalGate
    justification: Optional[str] = None
    approver_id: Optional[uuid.UUID] = None

class ExecutiveDecisionResponse(ExecutiveDecisionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    decided_at: Optional[datetime] = None
    class Config:
        from_attributes = True

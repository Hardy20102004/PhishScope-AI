from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.appsec_command_center import GovernanceDecisionStatus

# --- Executive Metric ---
class AppSecExecutiveMetricBase(BaseModel):
    enterprise_risk_score: float = 0.0
    compliance_posture: float = 0.0
    total_critical_vulnerabilities: int = 0

class AppSecExecutiveMetricCreate(AppSecExecutiveMetricBase):
    pass

class AppSecExecutiveMetricResponse(AppSecExecutiveMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    calculated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Engineering Productivity ---
class EngineeringProductivityMetricBase(BaseModel):
    application_id: str
    mean_time_to_remediate_days: float = 0.0
    deployment_frequency_per_week: float = 0.0
    security_friction_score: float = 0.0

class EngineeringProductivityMetricCreate(EngineeringProductivityMetricBase):
    pass

class EngineeringProductivityMetricResponse(EngineeringProductivityMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    calculated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Consolidated Finding ---
class AppSecConsolidatedFindingBase(BaseModel):
    application_id: str
    source_scanner: str
    severity: str = "MEDIUM"
    cwe_id: Optional[str] = None
    title: str
    description: str
    is_remediated: bool = False

class AppSecConsolidatedFindingCreate(AppSecConsolidatedFindingBase):
    pass

class AppSecConsolidatedFindingResponse(AppSecConsolidatedFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Governance Decision ---
class AppSecGovernanceDecisionBase(BaseModel):
    policy_name: str
    proposed_change: str
    status: GovernanceDecisionStatus = GovernanceDecisionStatus.PENDING

class AppSecGovernanceDecisionCreate(AppSecGovernanceDecisionBase):
    pass

class AppSecGovernanceDecisionResponse(AppSecGovernanceDecisionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    requested_by: uuid.UUID
    approved_by: Optional[uuid.UUID] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

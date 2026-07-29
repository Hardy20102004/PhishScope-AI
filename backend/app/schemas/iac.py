from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.iac import IaCTechnology, IaCDeploymentStatus

# --- IaC Template ---
class IaCTemplateBase(BaseModel):
    name: str
    technology: IaCTechnology = IaCTechnology.UNKNOWN
    repository_url: str
    file_path: str

class IaCTemplateCreate(IaCTemplateBase):
    pass

class IaCTemplateResponse(IaCTemplateBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- IaC Configuration Finding ---
class IaCConfigurationFindingBase(BaseModel):
    severity: str = "HIGH"
    category: str
    title: str
    description: str
    resource_id: Optional[str] = None
    line_number: Optional[int] = None

class IaCConfigurationFindingCreate(IaCConfigurationFindingBase):
    template_id: uuid.UUID

class IaCConfigurationFindingResponse(IaCConfigurationFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    template_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- IaC Policy ---
class IaCPolicyBase(BaseModel):
    name: str
    description: str
    is_active: bool = True

class IaCPolicyCreate(IaCPolicyBase):
    pass

class IaCPolicyResponse(IaCPolicyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- IaC Deployment Governance ---
class IaCDeploymentGovernanceBase(BaseModel):
    status: IaCDeploymentStatus = IaCDeploymentStatus.PENDING_APPROVAL
    risk_score: float = 0.0

class IaCDeploymentGovernanceCreate(IaCDeploymentGovernanceBase):
    template_id: uuid.UUID
    requested_by: uuid.UUID

class IaCDeploymentGovernanceResponse(IaCDeploymentGovernanceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    template_id: uuid.UUID
    requested_by: uuid.UUID
    approved_by: Optional[uuid.UUID] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# --- IaC Guidance ---
class IaCGuidanceBase(BaseModel):
    suggested_code: str
    explanation: str

class IaCGuidanceCreate(IaCGuidanceBase):
    finding_id: uuid.UUID

class IaCGuidanceResponse(IaCGuidanceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    finding_id: uuid.UUID
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Executive Summary ---
class IaCExecutiveSummary(BaseModel):
    total_templates: int
    critical_findings: int
    pending_deployments: int
    blocked_deployments: int

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class AttackSurfaceNodeBase(BaseModel):
    asset_id: str
    asset_type: str
    exposure_vector: str
    is_active: bool

class AttackSurfaceNodeResponse(AttackSurfaceNodeBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BusinessContextBoundaryBase(BaseModel):
    boundary_name: str
    boundary_type: str
    boundary_identifier: str
    business_criticality: str
    compliance_scope: Optional[str] = None

class BusinessContextBoundaryResponse(BusinessContextBoundaryBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CloudExposureFindingBase(BaseModel):
    attack_surface_node_id: uuid.UUID
    finding_type: str
    finding_name: str
    raw_severity: float
    contextual_risk_score: float
    status: str

class CloudExposureFindingResponse(CloudExposureFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RemediationPlanBase(BaseModel):
    exposure_id: uuid.UUID
    plan_title: str
    steps: Dict[str, Any]
    estimated_risk_reduction: float
    status: str

class RemediationPlanResponse(RemediationPlanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    governance_workflow_id: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

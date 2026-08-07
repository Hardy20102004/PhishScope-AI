import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional

class K8sClusterBase(BaseModel):
    cluster_name: str
    provider: str
    version: str
    region: str
    status: str

class K8sClusterResponse(K8sClusterBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class K8sRBACPolicyBase(BaseModel):
    cluster_id: uuid.UUID
    subject_name: str
    subject_type: str
    namespace: Optional[str] = None
    effective_permissions: Dict[str, Any]
    is_overprivileged: bool

class K8sRBACPolicyResponse(K8sRBACPolicyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    analyzed_at: datetime
    model_config = ConfigDict(from_attributes=True)

class K8sRiskScoreBase(BaseModel):
    cluster_id: uuid.UUID
    risk_score: float
    rbac_issues_count: int
    admission_issues_count: int

class K8sRiskScoreResponse(K8sRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from app.models.identity_command_center import (
    IdentityType, ApprovalStatus
)

# ─────────────────────────────────────────────────────────────────────────────
# Portfolio
# ─────────────────────────────────────────────────────────────────────────────
class EnterpriseIdentityPortfolioBase(BaseModel):
    identity_id: str
    identity_type: IdentityType
    is_privileged: bool = False
    is_federated: bool = False
    managed_by: Optional[str] = None

class EnterpriseIdentityPortfolioResponse(EnterpriseIdentityPortfolioBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_correlated_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Health Metrics
# ─────────────────────────────────────────────────────────────────────────────
class IdentityHealthMetricResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    auth_health: float
    privilege_health: float
    lifecycle_health: float
    federation_health: float
    zero_trust_health: float
    measured_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Decision Log
# ─────────────────────────────────────────────────────────────────────────────
class ExecutiveDecisionLogBase(BaseModel):
    decision_type: str
    justification: str
    approver_id: str
    metadata_context: Dict[str, Any] = Field(default_factory=dict)

class ExecutiveDecisionLogCreate(ExecutiveDecisionLogBase):
    pass

class ExecutiveDecisionLogResponse(ExecutiveDecisionLogBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: ApprovalStatus
    created_at: datetime
    resolved_at: Optional[datetime]
    class Config:
        from_attributes = True

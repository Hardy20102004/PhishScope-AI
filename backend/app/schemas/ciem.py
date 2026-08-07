import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class CloudIdentityBase(BaseModel):
    identity_name: str
    identity_type: str
    provider: str
    account_id: str
    status: str
    mfa_enabled: bool
    last_login: Optional[datetime] = None

class CloudIdentityResponse(CloudIdentityBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CloudEntitlementBase(BaseModel):
    identity_id: uuid.UUID
    resource_type: str
    action: str
    effect: str
    is_admin_privilege: bool

class CloudEntitlementResponse(CloudEntitlementBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    analyzed_at: datetime
    model_config = ConfigDict(from_attributes=True)

class IdentityRiskScoreBase(BaseModel):
    identity_id: uuid.UUID
    risk_score: float
    risk_factors: List[str]

class IdentityRiskScoreResponse(IdentityRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AccessReviewBase(BaseModel):
    identity_id: uuid.UUID
    status: str
    reviewer_id: Optional[uuid.UUID] = None
    notes: Optional[str] = None

class AccessReviewResponse(AccessReviewBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TenantSettingsUpdate(BaseModel):
    branding_json: Optional[dict] = None
    sso_config_json: Optional[dict] = None
    require_mfa: Optional[bool] = None
    session_timeout_minutes: Optional[int] = None

class TenantSettingsSchema(BaseModel):
    id: UUID
    organization_id: UUID
    branding_json: dict
    sso_config_json: dict
    require_mfa: bool
    session_timeout_minutes: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LicenseSchema(BaseModel):
    id: UUID
    organization_id: UUID
    plan_tier: str
    max_seats: int
    valid_until: datetime
    is_active: bool
    features_json: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AuditLogSchema(BaseModel):
    id: UUID
    organization_id: UUID
    user_id: Optional[UUID] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details_json: dict
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

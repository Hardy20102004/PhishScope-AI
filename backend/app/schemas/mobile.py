from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MobileEnrollmentRequest(BaseModel):
    device_id: str
    platform: str
    os_version: str
    is_biometric_enabled: bool
    push_token: Optional[str] = None

class SyncRequest(BaseModel):
    last_sync: Optional[datetime] = None
    offline_queue: list = []

class MobileDeviceSchema(BaseModel):
    id: UUID
    user_id: UUID
    device_id: str
    platform: str
    os_version: str
    is_biometric_enabled: bool
    is_compliant: bool
    sync_state_json: dict
    created_at: datetime
    last_sync_at: datetime

    model_config = ConfigDict(from_attributes=True)

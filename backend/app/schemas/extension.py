from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ExtensionDeviceRegister(BaseModel):
    browser_type: str
    device_fingerprint: str
    settings: dict = {}

class ExtensionDeviceSchema(BaseModel):
    id: UUID
    user_id: UUID
    browser_type: Optional[str]
    device_fingerprint: str
    is_active: bool
    settings: dict
    created_at: datetime
    last_active_at: datetime

    model_config = ConfigDict(from_attributes=True)

class QuickInvestigateRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    context_type: str # "URL", "TEXT", "IMAGE"

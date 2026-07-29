import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# History
class BrowserHistoryBase(BaseModel):
    url: str
    title: Optional[str]
    visit_count: int
    is_threat_hit: bool
    threat_category: Optional[str]
    timestamp: datetime

class BrowserHistoryResponse(BrowserHistoryBase):
    id: uuid.UUID
    profile_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Extensions
class BrowserExtensionBase(BaseModel):
    extension_id: str
    name: str
    version: str
    description: Optional[str]
    permissions: Optional[str]
    is_suspicious: bool
    install_time: Optional[datetime]

class BrowserExtensionResponse(BrowserExtensionBase):
    id: uuid.UUID
    profile_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Profiles
class BrowserProfileBase(BaseModel):
    browser_type: str
    profile_name: str
    host_os: str

class BrowserProfileCreate(BrowserProfileBase):
    investigation_id: Optional[uuid.UUID] = None

class BrowserProfileResponse(BrowserProfileBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    uploaded_at: datetime
    
    history_records: List[BrowserHistoryResponse] = []
    extensions: List[BrowserExtensionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

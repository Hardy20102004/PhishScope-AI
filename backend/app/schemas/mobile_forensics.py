import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Communications
class MobileCommunicationBase(BaseModel):
    app_name: str
    thread_id: str
    sender: str
    receiver: str
    body: str
    is_outgoing: bool
    is_deleted: bool
    timestamp: datetime

class MobileCommunicationResponse(MobileCommunicationBase):
    id: uuid.UUID
    device_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Locations
class MobileLocationBase(BaseModel):
    source: str
    latitude: float
    longitude: float
    accuracy_meters: Optional[float]
    timestamp: datetime

class MobileLocationResponse(MobileLocationBase):
    id: uuid.UUID
    device_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Mobile Devices
class MobileDeviceBase(BaseModel):
    device_name: str
    os_type: str
    os_version: str
    acquisition_type: str
    imei: Optional[str]

class MobileDeviceCreate(MobileDeviceBase):
    investigation_id: Optional[uuid.UUID] = None

class MobileDeviceResponse(MobileDeviceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    uploaded_at: datetime
    
    communications: List[MobileCommunicationResponse] = []
    locations: List[MobileLocationResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

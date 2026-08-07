import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Network Connections
class MemoryNetworkConnectionBase(BaseModel):
    pid: Optional[int]
    protocol: str
    local_ip: str
    local_port: int
    remote_ip: str
    remote_port: int
    state: str

class MemoryNetworkConnectionResponse(MemoryNetworkConnectionBase):
    id: uuid.UUID
    memory_image_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Processes
class MemoryProcessBase(BaseModel):
    pid: int
    ppid: int
    name: str
    is_hidden: bool
    is_injected: bool
    start_time: Optional[datetime]

class MemoryProcessResponse(MemoryProcessBase):
    id: uuid.UUID
    memory_image_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Memory Images
class MemoryImageBase(BaseModel):
    filename: str
    os_profile: str
    size_bytes: int

class MemoryImageCreate(MemoryImageBase):
    investigation_id: Optional[uuid.UUID] = None

class MemoryImageResponse(MemoryImageBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    uploaded_at: datetime
    
    processes: List[MemoryProcessResponse] = []
    network_connections: List[MemoryNetworkConnectionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

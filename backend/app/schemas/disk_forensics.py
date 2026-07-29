import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Forensic Artifacts
class ForensicArtifactBase(BaseModel):
    filepath: str
    is_deleted: bool
    is_carved: bool
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    accessed_at: Optional[datetime]

class ForensicArtifactResponse(ForensicArtifactBase):
    id: uuid.UUID
    partition_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Disk Partitions
class DiskPartitionBase(BaseModel):
    partition_type: str
    start_sector: int
    size_bytes: int

class DiskPartitionResponse(DiskPartitionBase):
    id: uuid.UUID
    disk_image_id: uuid.UUID
    artifacts: List[ForensicArtifactResponse] = []
    model_config = ConfigDict(from_attributes=True)

# Disk Images
class DiskImageBase(BaseModel):
    filename: str
    format: str
    size_bytes: int
    md5_hash: str
    sha256_hash: str

class DiskImageCreate(DiskImageBase):
    investigation_id: Optional[uuid.UUID] = None

class DiskImageResponse(DiskImageBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    hash_verified: bool
    uploaded_at: datetime
    
    partitions: List[DiskPartitionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

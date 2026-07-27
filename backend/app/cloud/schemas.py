from typing import Optional, List, Dict, Any
from pydantic import ConfigDict, BaseModel, Field
import uuid
from datetime import datetime

from app.cloud.models import TLPLevel, WorkspaceType

class TenantBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class TenantResponse(TenantBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class WorkspaceBase(BaseModel):
    name: str
    workspace_type: WorkspaceType = WorkspaceType.PRIVATE

class WorkspaceCreate(WorkspaceBase):
    tenant_id: uuid.UUID

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    workspace_type: Optional[WorkspaceType] = None

class WorkspaceResponse(WorkspaceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class WorkspaceMemberBase(BaseModel):
    user_id: uuid.UUID
    role: str = "VIEWER"

class WorkspaceMemberCreate(WorkspaceMemberBase):
    pass

class WorkspaceMemberResponse(WorkspaceMemberBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    added_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class SharingPolicyBase(BaseModel):
    name: str
    tlp_level: TLPLevel = TLPLevel.AMBER
    require_approval: bool = True
    anonymize_source: bool = True
    target_audiences: List[str] = Field(default_factory=list)
    expiration_days: Optional[int] = None

class SharingPolicyCreate(SharingPolicyBase):
    pass

class SharingPolicyResponse(SharingPolicyBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class SharedObjectCreate(BaseModel):
    entity_type: str
    entity_id: str
    payload: Dict[str, Any]
    tlp_level: TLPLevel
    confidence: int = 50

class SharedObjectResponse(SharedObjectCreate):
    id: uuid.UUID
    source_workspace_id: uuid.UUID
    version: int
    shared_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class FederationNodeBase(BaseModel):
    name: str
    url: str
    node_type: str = "PARTNER"
    auth_method: str = "MTLS"
    auth_config: Dict[str, Any] = Field(default_factory=dict)

class FederationNodeCreate(FederationNodeBase):
    pass

class FederationNodeResponse(FederationNodeBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class FederationSyncResponse(BaseModel):
    id: uuid.UUID
    node_id: uuid.UUID
    sync_type: str
    objects_synced: int
    conflicts_resolved: int
    status: str
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ConflictRecordResponse(BaseModel):
    id: uuid.UUID
    entity_id: str
    entity_type: str
    local_version: int
    remote_version: int
    resolution_strategy: str
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CloudAuditLogResponse(BaseModel):
    id: uuid.UUID
    tenant_id: Optional[uuid.UUID]
    user_id: uuid.UUID
    action: str
    resource_id: Optional[str]
    details: Dict[str, Any]
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CloudAnalyticsResponse(BaseModel):
    id: uuid.UUID
    metric_name: str
    metric_value: float
    dimensions: Dict[str, Any]
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


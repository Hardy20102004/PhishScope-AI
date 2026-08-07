import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class CloudAuditLogBase(BaseModel):
    event_name: str
    event_source: str
    actor_identity: str
    source_ip: str
    is_anomalous: bool
    anomaly_reason: Optional[str]
    raw_event: Dict[str, Any]
    timestamp: datetime

class ContainerMetadataBase(BaseModel):
    container_id: str
    image_name: str
    is_privileged: bool
    mounts_host_root: bool
    mounts_docker_sock: bool
    config_dump: Dict[str, Any]
    is_compromised: bool

class KubernetesPodBase(BaseModel):
    namespace: str
    pod_name: str
    service_account: str
    host_network: bool
    host_pid: bool
    raw_manifest: Dict[str, Any]

class CloudEnvironmentBase(BaseModel):
    provider: str
    account_id: Optional[str]
    region: Optional[str]

class CloudEnvironmentCreate(CloudEnvironmentBase):
    investigation_id: Optional[uuid.UUID] = None

class CloudEnvironmentResponse(CloudEnvironmentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    uploaded_at: datetime
    
    audit_logs: List[CloudAuditLogBase] = []
    containers: List[ContainerMetadataBase] = []
    kubernetes_pods: List[KubernetesPodBase] = []
    
    model_config = ConfigDict(from_attributes=True)

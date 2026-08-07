import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class AssetNodeBase(BaseModel):
    node_type: str
    name: str
    is_critical: bool
    properties: Dict[str, Any]

class AssetNodeResponse(AssetNodeBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

class AssetRelationshipBase(BaseModel):
    source_node_id: uuid.UUID
    target_node_id: uuid.UUID
    relationship_type: str

class AssetRelationshipResponse(AssetRelationshipBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

class SimulatedAttackPathBase(BaseModel):
    start_node_id: uuid.UUID
    target_node_id: uuid.UUID
    path_sequence: List[str]
    path_complexity: int

class SimulatedAttackPathResponse(SimulatedAttackPathBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

from typing import Optional, List, Dict, Any
from pydantic import ConfigDict, BaseModel
import uuid
from datetime import datetime

class GraphNode(BaseModel):
    id: str
    label: str
    type: str # 'Threat Actor', 'Campaign', 'IP', 'Domain'
    properties: Dict[str, Any] = {}
    confidence: float = 1.0

class GraphLink(BaseModel):
    source: str
    target: str
    type: str # 'USES', 'TARGETS'
    properties: Dict[str, Any] = {}
    confidence: float = 1.0

class GraphPayload(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]

class GraphSnapshotCreate(BaseModel):
    name: str
    description: Optional[str] = None
    graph_data: GraphPayload

class GraphSnapshotResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    graph_data: GraphPayload
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AttackPathBase(BaseModel):
    name: str
    source_entity_id: str
    target_entity_id: str
    path_sequence: List[str]
    confidence: float

class AttackPathResponse(AttackPathBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ImpactAnalysisResponse(BaseModel):
    id: uuid.UUID
    entity_id: str
    degree_centrality: float
    betweenness_centrality: float
    blast_radius: int
    computed_at: datetime

    model_config = ConfigDict(from_attributes=True)


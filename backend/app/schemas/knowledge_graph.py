from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.knowledge_graph import EntityStatus, RelationshipStatus

class GraphEntityBase(BaseModel):
    entity_type: str
    name: str
    confidence: Optional[float] = 1.0
    properties_json: Optional[Dict[str, Any]] = {}

class GraphEntityCreate(GraphEntityBase):
    pass

class GraphEntityResponse(GraphEntityBase):
    id: str
    tenant_id: Optional[str] = None
    status: EntityStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class GraphRelationshipBase(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str
    weight: Optional[float] = 1.0
    confidence: Optional[float] = 1.0
    properties_json: Optional[Dict[str, Any]] = {}

class GraphRelationshipCreate(GraphRelationshipBase):
    pass

class GraphRelationshipResponse(GraphRelationshipBase):
    id: str
    status: RelationshipStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class SubgraphResponse(BaseModel):
    entities: List[GraphEntityResponse]
    relationships: List[GraphRelationshipResponse]

class TraversalPath(BaseModel):
    nodes: List[GraphEntityResponse]
    edges: List[GraphRelationshipResponse]

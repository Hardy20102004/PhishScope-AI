from typing import Optional, List, Dict, Any
from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime

class GraphEntityBase(BaseModel):
    entity_type: str
    name: str
    tenant_id: Optional[str] = None
    confidence: float = 1.0
    properties_json: Dict[str, Any] = Field(default_factory=dict)
    observed_start: Optional[datetime] = None
    observed_end: Optional[datetime] = None

class GraphEntityCreate(GraphEntityBase):
    pass

class GraphEntityResponse(GraphEntityBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class GraphRelationshipBase(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str
    weight: float = 1.0
    confidence: float = 1.0
    is_inferred: bool = False
    properties_json: Dict[str, Any] = Field(default_factory=dict)
    observed_start: Optional[datetime] = None
    observed_end: Optional[datetime] = None

class GraphRelationshipCreate(GraphRelationshipBase):
    pass

class GraphRelationshipResponse(GraphRelationshipBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class GraphPathResponse(BaseModel):
    nodes: List[GraphEntityResponse]
    edges: List[GraphRelationshipResponse]

class GraphAnalyticsResponse(BaseModel):
    metric_name: str
    value: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)

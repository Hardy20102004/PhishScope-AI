from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.ai_memory import MemoryType, SecurityClassification, RelationType

class MemoryBase(BaseModel):
    title: str
    description: str
    memory_type: MemoryType = MemoryType.WORKING
    owner_id: Optional[str] = None
    case_id: Optional[str] = None
    investigation_id: Optional[str] = None
    security_classification: SecurityClassification = SecurityClassification.INTERNAL
    retention_policy: str = "default"
    confidence_score: float = 1.0
    source: Optional[str] = None
    # For evidence and threat references, we'll store them as standard edges or metadata
    metadata: Optional[Dict[str, Any]] = None

class MemoryCreate(MemoryBase):
    pass

class MemoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    security_classification: Optional[SecurityClassification] = None
    confidence_score: Optional[float] = None

class MemoryRelationshipResponse(BaseModel):
    id: str
    target_id: str
    relation_type: str
    weight: float

    class Config:
        from_attributes = True

class MemoryResponse(MemoryBase):
    id: str
    tenant_id: str
    organization_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime]
    version: int
    vector_id: Optional[str]
    relationships: List[MemoryRelationshipResponse] = []

    class Config:
        from_attributes = True

class RelationshipCreate(BaseModel):
    target_id: str
    relation_type: RelationType
    weight: float = 1.0

class MemorySearchQuery(BaseModel):
    query_text: Optional[str] = None
    semantic_search: bool = True
    filters: Optional[Dict[str, Any]] = None # e.g., {"memory_type": "CASE", "case_id": "123"}
    limit: int = 10

class MemoryAnalytics(BaseModel):
    total_memories: int
    memories_by_type: Dict[str, int]
    total_relationships: int
    vector_cache_hit_rate: float
    average_search_latency_ms: float

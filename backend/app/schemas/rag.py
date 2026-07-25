from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.rag import KnowledgeAssetStatus

class DocumentChunkResponse(BaseModel):
    id: str
    asset_id: str
    chunk_index: int
    content: str
    metadata_json: Dict[str, Any]
    
    model_config = ConfigDict(from_attributes=True)

class KnowledgeAssetBase(BaseModel):
    title: str
    source_type: str
    source_uri: Optional[str] = None
    author: Optional[str] = None
    metadata_json: Dict[str, Any] = {}

class KnowledgeAssetCreate(KnowledgeAssetBase):
    pass

class KnowledgeAssetResponse(KnowledgeAssetBase):
    id: str
    tenant_id: Optional[str] = None
    status: KnowledgeAssetStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class RAGSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    search_type: str = "hybrid" # hybrid, vector, keyword
    tenant_id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None

class RAGSearchResult(BaseModel):
    chunk_id: str
    asset_title: str
    content: str
    score: float
    metadata_json: Dict[str, Any]
    
class RAGSearchResponse(BaseModel):
    query: str
    results: List[RAGSearchResult]
    latency_ms: float

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.ai_memory import (
    MemoryCreate, MemoryUpdate, MemoryResponse, 
    MemorySearchQuery, RelationshipCreate, MemoryRelationshipResponse,
    MemoryAnalytics
)
from app.ai_memory.manager import MemoryManager
from app.ai_memory.search import HybridSearchEngine
from app.ai_memory.graph import RelationshipEngine
from app.models.ai_memory import MemoryItem, MemoryRelationship

router = APIRouter()

def get_memory_manager(db: Session = Depends(deps.get_db)) -> MemoryManager:
    return MemoryManager(db)

def get_search_engine(db: Session = Depends(deps.get_db)) -> HybridSearchEngine:
    return HybridSearchEngine(db)
    
def get_relationship_engine(db: Session = Depends(deps.get_db)) -> RelationshipEngine:
    return RelationshipEngine(db)

@router.post("/", response_model=MemoryResponse)
async def create_memory(
    data: MemoryCreate,
    manager: MemoryManager = Depends(get_memory_manager),
    relationship_engine: RelationshipEngine = Depends(get_relationship_engine)
):
    """Store a new structured memory item and index it semantically."""
    mem = manager.create_memory(data)
    
    # Transform to response format
    res = MemoryResponse.from_orm(mem)
    res.relationships = []
    return res

@router.post("/search", response_model=List[MemoryResponse])
async def search_memories(
    query: MemorySearchQuery,
    search_engine: HybridSearchEngine = Depends(get_search_engine),
    relationship_engine: RelationshipEngine = Depends(get_relationship_engine)
):
    """Retrieve memories using hybrid vector + keyword/filter search."""
    memories = search_engine.search(
        query_text=query.query_text,
        semantic=query.semantic_search,
        filters=query.filters,
        limit=query.limit
    )
    
    responses = []
    for m in memories:
        # Include 1-hop relationships in search results
        relations = relationship_engine.get_related_memories(m.id)
        res = MemoryResponse.from_orm(m)
        res.relationships = [MemoryRelationshipResponse(**r) for r in relations]
        responses.append(res)
        
    return responses

@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: str,
    manager: MemoryManager = Depends(get_memory_manager),
    relationship_engine: RelationshipEngine = Depends(get_relationship_engine)
):
    """Fetch a specific memory and its graph relationships."""
    mem = manager.get_memory(memory_id)
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")
        
    relations = relationship_engine.get_related_memories(memory_id)
    res = MemoryResponse.from_orm(mem)
    res.relationships = [MemoryRelationshipResponse(**r) for r in relations]
    return res

@router.post("/{memory_id}/relationships", response_model=MemoryRelationshipResponse)
async def link_memory(
    memory_id: str,
    link_data: RelationshipCreate,
    relationship_engine: RelationshipEngine = Depends(get_relationship_engine)
):
    """Create a directional edge between two memories in the Knowledge Graph."""
    rel = relationship_engine.link_memories(
        source_id=memory_id,
        target_id=link_data.target_id,
        relation_type=link_data.relation_type.value,
        weight=link_data.weight
    )
    return MemoryRelationshipResponse.from_orm(rel)

@router.get("/system/analytics", response_model=MemoryAnalytics)
async def get_analytics(db: Session = Depends(deps.get_db)):
    """Retrieve engine observability metrics."""
    total = db.query(MemoryItem).count()
    rels = db.query(MemoryRelationship).count()
    
    # Mock aggregation for types
    types = {}
    for m_type in db.query(MemoryItem.memory_type).distinct():
        count = db.query(MemoryItem).filter(MemoryItem.memory_type == m_type[0]).count()
        types[m_type[0]] = count
        
    return MemoryAnalytics(
        total_memories=total,
        memories_by_type=types,
        total_relationships=rels,
        vector_cache_hit_rate=0.92, # simulated metric
        average_search_latency_ms=45.2 # simulated metric
    )

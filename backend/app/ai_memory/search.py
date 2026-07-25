from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.ai_memory.embeddings import embedding_service, vector_store
from app.models.ai_memory import MemoryItem

logger = structlog.get_logger("phoenix.ai_memory.search")

class HybridSearchEngine:
    """
    Combines Keyword (SQL filtering) and Semantic (VectorStore) search for AI Memory Engine.
    """
    def __init__(self, db: Session):
        self.db = db

    def search(self, query_text: Optional[str] = None, semantic: bool = True, filters: Optional[Dict[str, Any]] = None, limit: int = 10) -> List[MemoryItem]:
        """
        Executes a hybrid search query.
        """
        logger.info("memory_hybrid_search", query=query_text, semantic=semantic)
        
        # 1. Semantic Search (Vector)
        vector_results = []
        if query_text and semantic:
            q_vec = embedding_service.generate_embedding(query_text)
            vector_results = vector_store.search(q_vec, top_k=limit * 2) # Fetch extra for filtering
            
        vector_ids = [res["vector_id"] for res in vector_results]
        
        # 2. Relational Query (Filters & Keyword fallback)
        sql_query = self.db.query(MemoryItem)
        
        if filters:
            for k, v in filters.items():
                if hasattr(MemoryItem, k) and v is not None:
                    sql_query = sql_query.filter(getattr(MemoryItem, k) == v)
                    
        # If semantic search was run, filter by the vector IDs
        if vector_ids:
            # We want memories that match the filters AND are in the semantic result set
            sql_query = sql_query.filter(MemoryItem.vector_id.in_(vector_ids))
        elif query_text and not semantic:
            # Fallback to basic ILIKE search if semantic is disabled
            search_pattern = f"%{query_text}%"
            sql_query = sql_query.filter(
                or_(
                    MemoryItem.title.ilike(search_pattern),
                    MemoryItem.description.ilike(search_pattern)
                )
            )
            
        memories = sql_query.limit(limit).all()
        
        # If semantic search was used, re-sort by the vector score
        if vector_ids:
            score_map = {res["vector_id"]: res["score"] for res in vector_results}
            memories.sort(key=lambda m: score_map.get(m.vector_id, 0.0), reverse=True)
            
        return memories

class ContextBuilder:
    """
    Optimizes retrieval for AI Agents.
    Compiles memories into a localized context window.
    """
    def __init__(self, db: Session):
        self.search_engine = HybridSearchEngine(db)
        
    def build_context_for_investigation(self, investigation_id: str) -> str:
        """Pulls all relevant evidence and notes for a specific investigation."""
        memories = self.search_engine.search(
            semantic=False,
            filters={"investigation_id": investigation_id},
            limit=50
        )
        context_parts = []
        for m in memories:
            context_parts.append(f"[{m.memory_type}] {m.title}: {m.description}")
        
        return "\n\n".join(context_parts)

import structlog
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.rag import KnowledgeAsset, DocumentChunk, KnowledgeAssetStatus
from app.schemas.rag import RAGSearchResult
from app.rag.embedding import EmbeddingService
from app.rag.ranking import RankingEngine

logger = structlog.get_logger("phoenix.rag.retrieval")

class HybridRetrievalEngine:
    def __init__(self, db: Session):
        self.db = db
        self.embedder = EmbeddingService()
        self.ranker = RankingEngine()

    def _cosine_similarity_mock(self, vec1: List[float], vec2: List[float]) -> float:
        """A simple cosine similarity for our mock vectors in SQLite."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot = sum(x*y for x, y in zip(vec1, vec2))
        norm1 = sum(x*x for x in vec1) ** 0.5
        norm2 = sum(x*x for x in vec2) ** 0.5
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def search(self, query: str, top_k: int = 5, search_type: str = "hybrid", tenant_id: Optional[str] = None) -> List[RAGSearchResult]:
        logger.info("executing_rag_search", query=query, type=search_type)
        
        # We fetch all active chunks (in production, we'd do this inside pgvector or elasticsearch!)
        base_query = self.db.query(DocumentChunk).join(KnowledgeAsset).filter(
            KnowledgeAsset.status == KnowledgeAssetStatus.ACTIVE
        )
        if tenant_id:
            base_query = base_query.filter(KnowledgeAsset.tenant_id == tenant_id)
            
        all_chunks = base_query.all()
        query_embedding = self.embedder.generate_embedding(query)
        
        results = []
        
        for chunk in all_chunks:
            score = 0.0
            
            # Vector Score
            if search_type in ["vector", "hybrid"]:
                if chunk.vector_embedding:
                    vec_score = self._cosine_similarity_mock(query_embedding, chunk.vector_embedding)
                    # Normalize to 0-1
                    vec_score = (vec_score + 1) / 2
                    score += vec_score * 0.7 # Weight vector 70% in hybrid
                    
            # Keyword Score
            if search_type in ["keyword", "hybrid"]:
                # Simple keyword match mock (BM25 in real system)
                query_terms = set(query.lower().split())
                chunk_terms = set(chunk.content.lower().split())
                overlap = len(query_terms.intersection(chunk_terms))
                kw_score = min(overlap / max(len(query_terms), 1), 1.0)
                
                if search_type == "keyword":
                    score = kw_score
                else:
                    score += kw_score * 0.3 # Weight keyword 30% in hybrid
                    
            if score > 0:
                results.append(RAGSearchResult(
                    chunk_id=chunk.id,
                    asset_title=chunk.asset.title,
                    content=chunk.content,
                    score=score,
                    metadata_json=chunk.metadata_json
                ))
                
        # Rank the results
        ranked_results = self.ranker.rank_results(results, query)
        
        return ranked_results[:top_k]

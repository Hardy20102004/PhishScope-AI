from app.rag.embedding import EmbeddingService
from app.rag.retrieval import HybridRetrievalEngine


def test_cosine_similarity_mock():
    # Mocking a session just to test the math
    engine = HybridRetrievalEngine(db=None)
    
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    assert engine._cosine_similarity_mock(vec1, vec2) == 1.0
    
    vec3 = [0.0, 1.0, 0.0]
    assert engine._cosine_similarity_mock(vec1, vec3) == 0.0

def test_embedding_determinism():
    service = EmbeddingService()
    v1 = service.generate_embedding("security threat")
    v2 = service.generate_embedding("security threat")
    assert v1 == v2
    assert len(v1) == 1536

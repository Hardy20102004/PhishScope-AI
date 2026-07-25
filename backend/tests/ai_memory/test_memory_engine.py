from app.ai_memory.graph import RelationshipEngine
from app.ai_memory.manager import MemoryManager
from app.ai_memory.search import HybridSearchEngine
from app.models.ai_memory import MemoryType, RelationType, SecurityClassification
from app.schemas.ai_memory import MemoryCreate


def test_memory_creation_and_search(db_session):
    manager = MemoryManager(db_session)
    search_engine = HybridSearchEngine(db_session)

    # Create memory 1
    m1_data = MemoryCreate(
        title="Malicious IP Alert",
        description="Detected communication with known C2 server at 192.168.1.50.",
        memory_type=MemoryType.THREAT_INTEL,
        security_classification=SecurityClassification.CONFIDENTIAL
    )
    m1 = manager.create_memory(m1_data)
    
    # Create memory 2
    m2_data = MemoryCreate(
        title="Phishing Campaign",
        description="Users reporting emails claiming to be from HR about Q3 bonuses.",
        memory_type=MemoryType.WORKING,
        security_classification=SecurityClassification.INTERNAL
    )
    m2 = manager.create_memory(m2_data)

    assert m1.id is not None
    assert m1.vector_id is not None
    assert m2.id is not None
    
    # Test semantic search
    results = search_engine.search(query_text="C2 server IP address", semantic=True)
    assert len(results) > 0
    # m1 should be highly ranked since it mentions C2 server
    assert any(r.id == m1.id for r in results)

def test_memory_relationships(db_session):
    manager = MemoryManager(db_session)
    graph = RelationshipEngine(db_session)

    m1 = manager.create_memory(MemoryCreate(title="Parent Case", description="Top level incident", memory_type=MemoryType.CASE))
    m2 = manager.create_memory(MemoryCreate(title="Child Evidence", description="Malware binary", memory_type=MemoryType.EVIDENCE))

    # Link them
    graph.link_memories(source_id=m1.id, target_id=m2.id, relation_type=RelationType.EVIDENCE.value, weight=1.5)

    # Get relations
    relations = graph.get_related_memories(m1.id)
    assert len(relations) == 1
    assert relations[0]["memory"]["id"] == m2.id
    assert relations[0]["relation_type"] == RelationType.EVIDENCE.value
    assert relations[0]["direction"] == "OUTGOING"

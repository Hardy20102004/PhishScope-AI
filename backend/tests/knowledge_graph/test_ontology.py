from app.knowledge_graph.ontology import OntologyManager


def test_ontology_validation():
    ontology = OntologyManager()
    
    # Test valid entities
    assert ontology.validate_entity_type("THREAT_ACTOR") == True
    assert ontology.validate_entity_type("IPV4") == True
    
    # Test invalid entity
    assert ontology.validate_entity_type("INVALID_TYPE") == False
    
    # Test valid relationship
    assert ontology.validate_relationship_type("BELONGS_TO") == True
    
    # Test invalid relationship
    assert ontology.validate_relationship_type("HATES") == False
    
    # Test valid triple
    assert ontology.is_valid_triple("THREAT_ACTOR", "TARGETS", "ORGANIZATION") == True

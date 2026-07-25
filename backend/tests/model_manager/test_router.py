import pytest
from app.model_manager.router import RoutingEngine
from app.models.model_manager import AIProvider, AIModel, RoutingPolicy

def test_routing_engine(db_session):
    # Setup Data
    provider = AIProvider(name="MockProvider")
    db_session.add(provider)
    db_session.commit()
    
    primary = AIModel(name="PrimaryModel", provider_id=provider.id, is_active=True, health_status="HEALTHY")
    fallback = AIModel(name="FallbackModel", provider_id=provider.id, is_active=True, health_status="HEALTHY")
    db_session.add_all([primary, fallback])
    db_session.commit()
    
    policy = RoutingPolicy(capability="TEST_CAPABILITY", primary_model_id=primary.id, fallback_model_id=fallback.id)
    db_session.add(policy)
    db_session.commit()
    
    engine = RoutingEngine(db_session)
    
    # Test 1: Routes to Primary
    res = engine.get_model_for_task("TEST_CAPABILITY")
    assert res.model.id == primary.id
    assert res.is_fallback is False
    
    # Test 2: Fallback when primary is unhealthy
    primary.health_status = "DOWN"
    db_session.commit()
    
    res = engine.get_model_for_task("TEST_CAPABILITY")
    assert res.model.id == fallback.id
    assert res.is_fallback is True
    
    # Test 3: Exception when both down
    fallback.is_active = False
    db_session.commit()
    
    with pytest.raises(ValueError):
        engine.get_model_for_task("TEST_CAPABILITY")

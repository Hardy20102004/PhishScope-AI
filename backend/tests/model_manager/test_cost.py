from app.model_manager.cost import CostManager
from app.models.model_manager import AIModel, AIProvider


def test_cost_manager(db_session):
    provider = AIProvider(name="CostProvider")
    db_session.add(provider)
    db_session.commit()
    
    model = AIModel(
        name="CostModel", 
        provider_id=provider.id,
        cost_per_1k_prompt=0.01,
        cost_per_1k_completion=0.03
    )
    db_session.add(model)
    db_session.commit()
    
    manager = CostManager(db_session)
    
    # 1000 prompt, 500 completion
    # Expected: (1000/1000 * 0.01) + (500/1000 * 0.03) = 0.01 + 0.015 = 0.025
    log = manager.log_usage(model.id, "TEST_TASK", 1000, 500)
    
    assert log.total_cost == 0.025

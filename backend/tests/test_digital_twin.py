import pytest
import uuid

from app.models.digital_twin import SimulationScenario
from app.digital_twin.simulation_engine import SimulationEngine
from app.digital_twin.optimization_engine import OptimizationEngine

pytestmark = pytest.mark.asyncio

async def test_simulation_execution(db_session):
    scenario = SimulationScenario(
        tenant_id=uuid.uuid4(),
        name="High Volume Stress Test",
        description="Testing MTTR under high load",
        alert_volume_multiplier=2.0, # 200% alerts
        analyst_headcount=10,
        automation_rate=0.5
    )
    
    db_session.add(scenario)
    await db_session.commit()
    
    engine = SimulationEngine(db_session)
    result = await engine.execute_scenario(scenario)
    
    assert result.id is not None
    # High volume should cause utilization to spike over 1.0
    assert result.analyst_utilization_rate > 1.0
    assert result.forecasted_sla_breach_rate > 0.05

async def test_optimization_generation(db_session):
    scenario = SimulationScenario(
        tenant_id=uuid.uuid4(),
        name="Bottleneck Scenario",
        description="",
        alert_volume_multiplier=3.0,
        analyst_headcount=5,
        automation_rate=0.2
    )
    db_session.add(scenario)
    await db_session.commit()
    
    sim_engine = SimulationEngine(db_session)
    result = await sim_engine.execute_scenario(scenario)
    
    opt_engine = OptimizationEngine(db_session)
    recommendations = await opt_engine.generate_recommendations(result)
    
    assert len(recommendations) > 0
    assert any(r.category == "STAFFING" for r in recommendations)
    assert any(r.category == "AUTOMATION" for r in recommendations)

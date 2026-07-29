import pytest
import uuid
from app.bas_platform.simulation_manager import SimulationManager
from app.bas_platform.scoring_engine import ScoringEngine
from app.bas_platform.validation_engine import ValidationEngine
from app.models.bas_platform import BasSimulation, BasValidationResult

pytestmark = pytest.mark.asyncio

async def test_scenario_creation_and_scoring(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Create Scenario
    mgr = SimulationManager(db_session)
    scenario = await mgr.create_scenario(
        tenant_id=tenant_id,
        name="Spearphishing Execution",
        description="Test execution of malicious macros.",
        tactic="Initial Access",
        technique_id="T1566.001",
        steps=[{"action": "drop_payload", "target": "C:\\temp\\macro.exe"}]
    )
    assert scenario.id is not None
    
    # 2. Execute Simulation
    simulation = await mgr.execute_simulation(tenant_id, scenario.id)
    assert simulation.status == "RUNNING"
    
    # 3. Simulate detection of half the steps
    val_eng = ValidationEngine(db_session)
    await val_eng.validate_simulation(simulation.id)
    
    # 4. Score the simulation
    score_eng = ScoringEngine(db_session)
    final_sim = await score_eng.finalize_simulation_score(simulation.id)
    
    assert final_sim.status == "COMPLETED"
    # The validation engine mocks 2 steps, 1 detected, 1 missed. Score should be 50.0
    assert final_sim.overall_score == 50.0

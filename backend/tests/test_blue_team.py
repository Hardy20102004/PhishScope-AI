import pytest
import uuid
from app.blue_team.readiness_manager import ReadinessManager
from app.blue_team.detection_validation import DetectionValidationEngine
from app.blue_team.analyst_readiness import AnalystReadinessEngine

pytestmark = pytest.mark.asyncio

async def test_maturity_score_aggregation(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Seed some detection metrics
    det_eng = DetectionValidationEngine(db_session)
    await det_eng.evaluate_rule_health(tenant_id, "Rule 1", "R-01", "Splunk", 100, 2) # NOISY
    await det_eng.evaluate_rule_health(tenant_id, "Rule 2", "R-02", "CS", 1, 10) # HEALTHY
    
    # 2. Seed some analyst metrics
    an_eng = AnalystReadinessEngine(db_session)
    await an_eng.log_team_metrics(tenant_id, "Tier 1", "W30", 12.0, 45.0, 95.0)
    
    # 3. Request Readiness Snapshot
    mgr = ReadinessManager(db_session)
    snapshot = await mgr.get_current_readiness(tenant_id)
    
    # Rule 1 is noisy, 50% noisy rate -> det score 50
    # Analyst score -> max(0, 100 - 12) = 88
    # Overall = (50 * 0.5) + (88 * 0.5) = 69.0
    
    assert snapshot.overall_maturity_score == 69.0
    assert snapshot.detection_health_score == 50.0
    assert snapshot.analyst_readiness_score == 88.0

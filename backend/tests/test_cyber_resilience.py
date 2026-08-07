import pytest
import uuid
from app.cyber_resilience.scoring_engine import SecurityScoringEngine
from app.cyber_resilience.maturity_engine import MaturityAssessmentEngine
from app.cyber_resilience.kpi_engine import ExecutiveKPIEngine

pytestmark = pytest.mark.asyncio

async def test_cyber_resilience_scoring(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Maturity Calculation
    me = MaturityAssessmentEngine(db_session)
    soc_mat = await me.calculate_domain_maturity(tenant_id, "SOC Operations", 86.0) # Should be tier 5
    det_mat = await me.calculate_domain_maturity(tenant_id, "Detection Engineering", 60.0) # Should be tier 3
    
    assert soc_mat.maturity_tier == 5
    assert det_mat.maturity_tier == 3
    
    # 2. Test Apex Score Calculation
    se = SecurityScoringEngine(db_session)
    score = await se.generate_resilience_score(tenant_id, prev_eff=90.0, det_eff=80.0, res_eff=85.0)
    
    expected_overall = (90.0 * 0.4) + (80.0 * 0.3) + (85.0 * 0.3)
    assert score.overall_readiness_score == expected_overall
    
    # 3. Test KPI Logging
    ke = ExecutiveKPIEngine(db_session)
    kpi = await ke.log_kpi(tenant_id, "MTTD", 4.2, "Hours", "-12% (Improving)")
    
    assert kpi.metric_name == "MTTD"
    assert kpi.metric_value == 4.2

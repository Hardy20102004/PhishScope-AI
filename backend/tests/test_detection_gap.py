import pytest
import uuid
from app.detection_gap.coverage_engine import CoverageAnalysisEngine
from app.detection_gap.gap_analysis_engine import GapAnalysisEngine
from app.detection_gap.optimization_engine import OptimizationEngine

pytestmark = pytest.mark.asyncio

async def test_gap_detection_logic(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Seed some coverage metrics
    ce = CoverageAnalysisEngine(db_session)
    await ce.log_coverage_metric(tenant_id, "TA0002", "T1059", "Command and Scripting", 85.0) # Good coverage
    await ce.log_coverage_metric(tenant_id, "TA0005", "T1562.001", "Disable Windows Event Logging", 0.0) # Blind spot
    await ce.log_coverage_metric(tenant_id, "TA0010", "T1048.003", "Exfiltration Over Alt Protocol", 12.0) # Weak coverage
    
    # 2. Test Overall Coverage calculation
    overall = await ce.get_overall_coverage(tenant_id)
    assert overall == (85.0 + 0.0 + 12.0) / 3
    
    # 3. Test Gap Analysis
    ge = GapAnalysisEngine(db_session)
    gaps = await ge.analyze_gaps(tenant_id)
    
    # Should only flag the ones < 30%
    assert len(gaps) == 2
    techs = [g.technique_id for g in gaps]
    assert "T1562.001" in techs
    assert "T1048.003" in techs
    
    # Check severity logic (0.0 is CRITICAL, <30 is HIGH)
    for g in gaps:
        if g.technique_id == "T1562.001":
            assert g.severity == "CRITICAL"
        elif g.technique_id == "T1048.003":
            assert g.severity == "HIGH"

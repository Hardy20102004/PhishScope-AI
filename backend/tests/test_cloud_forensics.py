import pytest
import uuid
from app.cloud_forensics.evidence_manager import EvidenceManager
from app.cloud_forensics.audit_engine import AuditEngine
from app.cloud_forensics.container_engine import ContainerEngine
from app.cloud_forensics.kubernetes_engine import KubernetesEngine

pytestmark = pytest.mark.asyncio

async def test_environment_registration(db_session):
    tenant_id = uuid.uuid4()
    mgr = EvidenceManager(db_session)
    
    env = await mgr.register_environment(
        tenant_id=tenant_id,
        provider="AWS",
        account_id="123456789012",
        region="us-east-1"
    )
    
    assert env.id is not None
    assert env.provider == "AWS"

async def test_audit_engine(db_session):
    engine = AuditEngine(db_session)
    env_id = uuid.uuid4()
    
    logs = await engine.analyze_logs(env_id=env_id)
    
    assert len(logs) > 0
    # Ensure anomaly detection works
    anomalies = [log for log in logs if log.is_anomalous]
    assert len(anomalies) > 0
    assert anomalies[0].event_name == "CreateAccessKey"

async def test_container_engine(db_session):
    engine = ContainerEngine(db_session)
    env_id = uuid.uuid4()
    
    containers = await engine.analyze_containers(env_id=env_id)
    assert len(containers) > 0
    
    # Ensure privileged container escape detection works
    compromised = [c for c in containers if c.is_compromised]
    assert len(compromised) > 0
    assert compromised[0].is_privileged is True

async def test_kubernetes_engine(db_session):
    engine = KubernetesEngine(db_session)
    env_id = uuid.uuid4()
    
    pods = await engine.analyze_kubernetes(env_id=env_id)
    assert len(pods) > 0
    assert pods[0].host_network is True

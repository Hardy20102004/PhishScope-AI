import pytest
import uuid
from app.cdr.telemetry_normalization_engine import TelemetryNormalizationEngine
from app.cdr.cloud_detection_engine import CloudDetectionEngine
from app.cdr.cloud_correlation_engine import CloudCorrelationEngine
from app.cdr.response_coordination_engine import ResponseCoordinationEngine

pytestmark = pytest.mark.asyncio

async def test_cdr_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Telemetry Ingestion
    tne = TelemetryNormalizationEngine(db_session)
    raw_event = {
        "responseElements": {"ConsoleLogin": "Success"},
        "additionalEventData": {"MFAUsed": "No"}
    }
    event = await tne.ingest_event(
        tenant_id, "AWS", "cloudtrail.amazonaws.com", "ConsoleLogin", raw_event, principal_id="bob_admin"
    )
    
    assert event.event_name == "ConsoleLogin"
    assert event.principal_id == "bob_admin"
    
    # 2. Test Detection
    cde = CloudDetectionEngine(db_session)
    detection = await cde.analyze_event(event)
    
    assert detection is not None
    assert detection.severity == "HIGH"
    
    # 3. Test Correlation
    cce = CloudCorrelationEngine(db_session)
    investigation = await cce.correlate_detection(detection, event)
    
    assert investigation is not None
    assert investigation.primary_entity == "bob_admin"
    assert detection.investigation_id == investigation.id
    
    # 4. Test Response Generation
    rce = ResponseCoordinationEngine(db_session)
    action = await rce.propose_containment(investigation)
    
    assert action.action_type == "REVOKE_IAM_SESSIONS"
    assert action.target_entity == "bob_admin"

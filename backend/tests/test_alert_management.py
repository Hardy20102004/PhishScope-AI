import pytest
import uuid
from httpx import AsyncClient

from app.models.alert_management import Alert, AlertEvidence, AlertLifecycleEvent
from app.alert_management.normalization import AlertNormalizationEngine
from app.alert_management.prioritization import AlertPrioritizationEngine

pytestmark = pytest.mark.asyncio

async def test_alert_normalization():
    raw_payload = {
        "title": "Malware Detected",
        "description": "Suspicious file execution",
        "severity": "CRITICAL",
        "category": "Malware",
        "source_ip": "192.168.1.100",
        "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
    
    tenant_id = uuid.uuid4()
    normalized = AlertNormalizationEngine.normalize_alert(raw_payload, "CrowdStrike", tenant_id)
    
    assert normalized["title"] == "Malware Detected"
    assert normalized["severity"] == "CRITICAL"
    assert normalized["source"] == "CrowdStrike"
    
    evidence = normalized["evidence"]
    assert len(evidence) == 2
    assert evidence[0]["evidence_type"] == "IP"
    assert evidence[0]["value"] == "192.168.1.100"
    assert evidence[1]["evidence_type"] == "HASH"

async def test_alert_prioritization():
    normalized_data = {
        "severity": "HIGH",
        "evidence": [{}, {}, {}] # 3 pieces of evidence
    }
    
    scores = AlertPrioritizationEngine.calculate_scores(normalized_data)
    
    # Priority = (Risk * 0.7) + (Confidence * 0.3)
    # Severity High = 6.0, Criticality = 5.0 -> Risk = 6 * 5 * 2 = 60
    # Confidence = 50 + (3 * 10) = 80
    # Priority = (60 * 0.7) + (80 * 0.3) = 42 + 24 = 66
    
    assert scores["risk_score"] == 60.0
    assert scores["confidence"] == 80.0
    assert scores["priority_score"] == 66.0

from app.main import app

from app.api.deps import get_current_active_user, get_async_db
from app.models.user import User
from app.db.session import SessionLocal
from tests.conftest import AsyncMockSession

async def mock_get_current_active_user():
    user = User()
    user.id = uuid.uuid4()
    user.tenant_id = uuid.uuid4()
    return user

async def mock_get_async_db():
    db = SessionLocal()
    try:
        yield AsyncMockSession(db)
    finally:
        db.close()

app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
app.dependency_overrides[get_async_db] = mock_get_async_db

async def test_ingest_alert_api(async_client: AsyncClient):
    payload = {
        "title": "Test SIEM Alert",
        "description": "Possible exfiltration",
        "source": "Splunk",
        "source_alert_id": "SPL-1001",
        "category": "Exfiltration",
        "severity": "MEDIUM",
        "tenant_id": str(uuid.uuid4()) # In real test this uses the test tenant
    }
    
    response = await async_client.post(
        "/api/v1/alerts/",
        json=payload,
        headers={"Authorization": "Bearer TEST_TOKEN"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test SIEM Alert"
    assert data["status"] == "NEW"
    assert "priority_score" in data

import pytest
from app.mobile_investigation.engines.timeline import TimelineEngine
from app.mobile_investigation.engines.ioc import IOCExtractionEngine
from app.mobile_investigation.engines.risk import RiskAssessmentEngine

def test_timeline_engine():
    comms = [
        {"timestamp": "2024-01-02T10:00:00Z", "comm_type": "SMS", "direction": "Incoming", "contact_number": "123", "body": "test"}
    ]
    locs = [
        {"timestamp": "2024-01-01T10:00:00Z", "latitude": 0, "longitude": 0, "label": "Home"}
    ]
    
    timeline = TimelineEngine.build(comms, locs)
    
    # Check chronological ordering
    assert len(timeline) == 2
    assert timeline[0]["event_type"] == "LocationUpdate"
    assert timeline[1]["event_type"] == "SMS"

def test_ioc_engine():
    comms = [
        {"timestamp": "2024-01-02T10:00:00Z", "comm_type": "SMS", "contact_number": "+15551234567", "body": "Go to http://evil.com/login"}
    ]
    
    iocs = IOCExtractionEngine.extract(comms)
    
    url_iocs = [i["ioc_value"] for i in iocs if i["ioc_type"] == "url"]
    phone_iocs = [i["ioc_value"] for i in iocs if i["ioc_type"] == "phone_number"]
    
    assert "http://evil.com/login" in url_iocs
    assert "+15551234567" in phone_iocs

def test_risk_scoring_engine():
    apps = [{"is_suspicious": True}, {"is_suspicious": False}] # +30
    iocs = [{"ioc_type": "url"}, {"ioc_type": "url"}] # +30
    
    result = RiskAssessmentEngine.calculate(apps, iocs)
    
    # 30 + 30 = 60 -> HIGH
    assert result["overall_risk_score"] == 60
    assert result["threat_severity"] == "HIGH"

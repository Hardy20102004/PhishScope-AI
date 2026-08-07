from app.cloud_investigation.engines.ioc import IOCExtractionEngine
from app.cloud_investigation.engines.risk import RiskAssessmentEngine
from app.cloud_investigation.engines.timeline import TimelineEngine


def test_timeline_engine():
    audits = [
        {"timestamp": "2024-01-02T10:00:00Z", "event_name": "DeleteTrail", "actor": "bob"}
    ]
    
    timeline = TimelineEngine.build([], [], [], audits)
    
    # Check chronological ordering
    assert len(timeline) == 1
    assert timeline[0]["event_type"] == "Audit"
    assert "DeleteTrail" in timeline[0]["description"]

def test_ioc_engine():
    audits = [
        {"source_ip": "1.2.3.4", "event_name": "ConsoleLogin", "actor": "admin"}
    ]
    
    iocs = IOCExtractionEngine.extract(audits)
    
    ips = [i["ioc_value"] for i in iocs if i["ioc_type"] == "ip"]
    actors = [i["ioc_value"] for i in iocs if i["ioc_type"] == "cloud_id"]
    
    assert "1.2.3.4" in ips
    assert "admin" in actors

def test_risk_scoring_engine():
    assets = [{"is_public": True}] # +10
    identities = [{"is_highly_privileged": True}] # +20
    configs = [{"is_misconfigured": True}] # +30
    audits = [{"is_anomalous": True}] # +50
    
    result = RiskAssessmentEngine.calculate(assets, identities, configs, audits)
    
    # 10 + 20 + 30 + 50 = 110 -> 100 max -> CRITICAL
    assert result["overall_risk_score"] == 100
    assert result["threat_severity"] == "CRITICAL"

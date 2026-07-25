import pytest
from app.network_investigation.engines.timeline import TimelineEngine
from app.network_investigation.engines.ioc import IOCExtractionEngine
from app.network_investigation.engines.risk import RiskAssessmentEngine

def test_timeline_engine():
    flows = [
        {"timestamp": "2024-01-02T10:00:00Z", "source_ip": "1.1.1.1", "destination_ip": "2.2.2.2"}
    ]
    dns = [
        {"timestamp": "2024-01-01T10:00:00Z", "query": "test.com"}
    ]
    http = [
        {"timestamp": "2024-01-03T10:00:00Z", "method": "GET", "host": "test.com"}
    ]
    tls = []
    
    timeline = TimelineEngine.build(flows, dns, http, tls)
    
    # Check chronological ordering
    assert len(timeline) == 3
    assert timeline[0]["event_type"] == "DNS"
    assert timeline[1]["event_type"] == "Flow"
    assert timeline[2]["event_type"] == "HTTP"

def test_ioc_engine():
    dns = [
        {"query": "evil.com", "answers": ["192.168.1.1"]}
    ]
    http = [
        {"host": "c2.evil.com", "uri": "/beacon"}
    ]
    tls = [
        {"server_name": "sni.evil.com"}
    ]
    
    iocs = IOCExtractionEngine.extract(dns, http, tls)
    
    domains = [i["ioc_value"] for i in iocs if i["ioc_type"] == "domain"]
    ips = [i["ioc_value"] for i in iocs if i["ioc_type"] == "ip"]
    urls = [i["ioc_value"] for i in iocs if i["ioc_type"] == "url"]
    
    assert "evil.com" in domains
    assert "c2.evil.com" in domains
    assert "sni.evil.com" in domains
    assert "192.168.1.1" in ips
    assert "http://c2.evil.com/beacon" in urls

def test_risk_scoring_engine():
    dns = [{"is_malicious": True}] # +40
    http = [{"method": "POST", "user_agent": "Windows NT"}] # +10
    
    result = RiskAssessmentEngine.calculate(dns, http)
    
    # 40 + 10 = 50 -> MEDIUM
    assert result["overall_risk_score"] == 50
    assert result["threat_severity"] == "MEDIUM"

import pytest
from app.browser_investigation.engines.timeline import TimelineEngine
from app.browser_investigation.engines.ioc import IOCExtractionEngine
from app.browser_investigation.engines.risk import RiskAssessmentEngine

def test_timeline_engine():
    history = [
        {"visit_time": "2024-01-02T10:00:00Z", "url": "http://test.com", "is_search": False}
    ]
    cookies = [
        {"creation_time": "2024-01-01T10:00:00Z", "domain": ".test.com", "name": "sess"}
    ]
    downloads = [
        {"download_time": "2024-01-03T10:00:00Z", "filename": "test.exe", "source_url": "http://test.com/test.exe"}
    ]
    
    timeline = TimelineEngine.build(history, cookies, downloads)
    
    # Check chronological ordering
    assert len(timeline) == 3
    assert timeline[0]["event_type"] == "CookieCreated"
    assert timeline[1]["event_type"] == "Visit"
    assert timeline[2]["event_type"] == "Download"

def test_ioc_engine():
    history = [
        {"url": "http://evil.com/login", "is_search": True, "search_keyword": "fake bank"}
    ]
    downloads = [
        {"source_url": "http://drop.evil.com/payload.exe"}
    ]
    
    iocs = IOCExtractionEngine.extract(history, downloads)
    
    url_iocs = [i["ioc_value"] for i in iocs if i["ioc_type"] == "url"]
    search_iocs = [i["ioc_value"] for i in iocs if i["ioc_type"] == "search_keyword"]
    
    assert "http://evil.com/login" in url_iocs
    assert "http://drop.evil.com/payload.exe" in url_iocs
    assert "fake bank" in search_iocs

def test_risk_scoring_engine():
    exts = [{"is_suspicious": True}, {"is_suspicious": False}] # +40
    dls = [{"is_malicious": True}] # +50
    
    result = RiskAssessmentEngine.calculate(exts, dls)
    
    # 40 + 50 = 90 -> CRITICAL
    assert result["overall_risk_score"] == 90
    assert result["threat_severity"] == "CRITICAL"

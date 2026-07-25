import pytest
from app.url_intelligence.engines.parser import URLParser
from app.url_intelligence.engines.normalizer import URLNormalizationEngine
from app.url_intelligence.engines.intelligence import URLIntelligenceEngine
from app.url_intelligence.engines.brand import BrandProtectionEngine

def test_url_parser():
    url = "https://sub.example.com:8443/path?a=1&b=2#frag"
    parsed = URLParser.parse(url)
    
    assert parsed["protocol"] == "https"
    assert parsed["hostname"] == "sub.example.com"
    assert parsed["subdomain"] == "sub"
    assert parsed["root_domain"] == "example.com"
    assert parsed["port"] == 8443
    assert parsed["path"] == "/path"
    assert "a" in parsed["query_parameters"]

def test_url_normalizer():
    url = "HTTP://EXAMPLE.COM/a/./b/../c?b=2&a=1&a=1"
    canonical = URLNormalizationEngine.normalize(url)
    assert canonical == "http://example.com/a/c?a=1&b=2"

def test_intelligence_engine():
    url = "http://login.paypal.secure-auth-example.com/verify?email=test@test.com"
    parsed = URLParser.parse(url)
    intel = URLIntelligenceEngine.analyze(url, parsed)
    
    assert "login" in intel["suspicious_keywords_found"]
    assert "verify" in intel["suspicious_keywords_found"]

def test_brand_protection_engine():
    hostname = "microsoft-login.example.com"
    root_domain = "example.com"
    
    brand_data = BrandProtectionEngine.analyze(hostname, root_domain)
    # The current logic checks the root_domain. 'example.com' won't trigger 'microsoft'.
    assert not brand_data["is_typosquat"]
    
    root_domain2 = "micros0ft.com"
    hostname2 = "micros0ft.com"
    brand_data2 = BrandProtectionEngine.analyze(hostname2, root_domain2)
    assert brand_data2["is_typosquat"]
    assert brand_data2["typosquat_target"] == "microsoft"

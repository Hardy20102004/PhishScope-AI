import pytest
from app.website_investigation.engines.html import HTMLAnalysisEngine
from app.website_investigation.engines.javascript import JavaScriptAnalysisEngine
from app.website_investigation.engines.forms_cookies import FormAnalysisEngine, CookieAnalysisEngine
from app.website_investigation.engines.security import SecurityHeaderAnalyzer

def test_html_engine():
    html_mock = """
    <html>
    <head><meta http-equiv="refresh" content="0; url=http://evil.com"></head>
    <body>
    <div style="display: none">Hidden text</div>
    <!-- password: password123 -->
    <iframe src="http://hidden.com"></iframe>
    </body>
    </html>
    """
    results = HTMLAnalysisEngine.analyze(html_mock)
    
    assert results["has_meta_refresh"]
    assert results["has_hidden_elements"]
    assert results["has_iframes"]
    assert results["embedded_credentials"]

def test_javascript_engine():
    scripts = [
        {"type": "inline", "content": "eval('alert(1)'); navigator.clipboard.readText();"},
        {"type": "external", "src": "https://google-analytics.com/analytics.js"}
    ]
    results = JavaScriptAnalysisEngine.analyze(scripts)
    
    assert len(results) == 2
    assert results[0]["uses_suspicious_apis"]
    assert results[0]["accesses_clipboard"]
    assert not results[0]["is_tracking_library"]
    
    assert results[1]["is_tracking_library"]

def test_form_engine():
    forms = [
        {
            "action": "/login",
            "inputs": [
                {"name": "username", "type": "text"},
                {"name": "pass", "type": "password"}
            ]
        }
    ]
    results = FormAnalysisEngine.analyze(forms)
    
    assert results[0]["is_login"]
    assert results[0]["has_password_field"]
    assert not results[0]["has_credit_card_field"]

def test_security_analyzer():
    headers = {
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "DENY"
    }
    
    results = SecurityHeaderAnalyzer.analyze(headers)
    assert results["strict_transport_security"] == "max-age=31536000"
    assert results["x_frame_options"] == "DENY"
    assert not results["content_security_policy"]

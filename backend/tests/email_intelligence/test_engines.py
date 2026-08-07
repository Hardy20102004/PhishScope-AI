from app.email_intelligence.engines.attachments import AttachmentIntelligenceEngine
from app.email_intelligence.engines.auth import AuthenticationAnalysisEngine
from app.email_intelligence.engines.conversation import ConversationAnalysisEngine
from app.email_intelligence.engines.parser import EmailParserEngine


def test_parser_engine():
    raw_eml = """Date: Mon, 25 Jul 2026 10:00:00 +0000
From: "Test" <test@example.com>
Subject: Hello
Content-Type: text/plain

This is a test body.
"""
    result = EmailParserEngine.parse(raw_eml)
    assert not result["error"]
    assert "Test" in result["headers"]["From"]
    assert "This is a test body." in result["body_text"]

def test_auth_engine():
    headers = {
        "Authentication-Results": "mx.google.com; spf=fail smtp.mailfrom=ceo@example.com; dmarc=fail"
    }
    result = AuthenticationAnalysisEngine.analyze(headers)
    assert result["spf_result"] == "fail"
    assert result["dmarc_result"] == "fail"
    assert result["is_spoofed"]

def test_conversation_engine():
    body = "Please process this urgent invoice immediately. Visit http://malicious.com"
    result = ConversationAnalysisEngine.analyze(body, "")
    assert result["is_bec_suspect"]
    assert len(result["extracted_urls"]) == 1
    assert result["extracted_urls"][0]["url"] == "http://malicious.com"

def test_attachment_engine():
    attachments = [
        {"filename": "invoice.exe", "content_type": "application/x-msdownload", "size": 1024, "raw_payload": b"123"}
    ]
    result = AttachmentIntelligenceEngine.analyze(attachments)
    assert result[0]["is_suspicious"]
    assert result[0]["sha256_hash"] != ""

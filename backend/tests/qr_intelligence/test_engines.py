import pytest
from app.qr_intelligence.engines.decoder import QRDecoderEngine
from app.qr_intelligence.engines.payment import PaymentQRAnalyzer
from app.qr_intelligence.engines.tampering import TamperingDetectionEngine

def test_decoder_engine():
    result = QRDecoderEngine.decode("https://example.com")
    assert result["payload_type"] == "url"
    assert result["extracted_url"] == "https://example.com"
    
    result_upi = QRDecoderEngine.decode("upi://pay?pa=test@bank")
    assert result_upi["payload_type"] == "payment_upi"

def test_payment_engine():
    decoded = {"raw_payload": "upi://pay?pa=test@bank&am=100", "payload_type": "payment_upi"}
    result = PaymentQRAnalyzer.analyze(decoded)
    assert result["payment_network"] == "UPI"
    assert result["merchant_id"] == "test@bank"
    assert result["transaction_amount"] == 100
    assert result["is_dynamic"]

def test_tampering_engine():
    decoded = {"raw_payload": "tampered payload with sticker"}
    result = TamperingDetectionEngine.analyze(decoded)
    assert result["has_overlay_sticker"]
    assert result["tampering_confidence"] > 0.9

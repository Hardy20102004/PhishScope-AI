import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class QRAIIntegration:
    """
    Integrates QR Intelligence with PHOENIX AI Brain to generate explainable risk narratives.
    """
    
    @staticmethod
    async def generate_narrative(decoded: dict, visual: dict, tampering: dict, payment: dict, risk: dict) -> Dict[str, str]:
        
        narrative = f"Investigation of QR code yields a {risk.get('threat_severity')} threat level (Score: {risk.get('overall_risk_score')}/100). "
        
        threat_summary = []
        
        # Tampering
        if tampering.get("has_overlay_sticker"):
            narrative += "Computer vision detected high contrast edges consistent with an overlay sticker physically placed on top of the original QR code. "
            threat_summary.append("Physical Tampering (Sticker)")
            
        if tampering.get("has_logo_anomaly"):
            narrative += "The central brand logo appears disjointed from the surrounding error-correction blocks, indicating potential image manipulation. "
            threat_summary.append("Visual Anomaly")
            
        # Payload Analysis
        if decoded.get("payload_type") == "url":
            narrative += f"The QR embeds a URL ({decoded.get('extracted_url')}). "
            if risk.get("url_risk") > 30:
                narrative += "The embedded URL is flagged as highly suspicious by the URL Intelligence Platform. "
                threat_summary.append("Malicious Embedded URL")
                
        elif decoded.get("payload_type") == "payment_upi":
            narrative += f"The QR initiates a UPI transaction (Merchant: {payment.get('merchant_id')}). "
            if payment.get("is_dynamic"):
                narrative += f"The transaction specifies a fixed amount of {payment.get('transaction_amount')} {payment.get('currency')}. "
            
            if tampering.get("has_overlay_sticker"):
                narrative += "WARNING: This is a classic 'Quishing' (QR Phishing) attack where a legitimate merchant's payment code has been overlaid with the attacker's UPI address. "
                threat_summary.append("Payment Fraud (Quishing)")
                
        if not threat_summary:
            if risk.get("overall_risk_score", 0) < 30:
                narrative += "The QR code payload is benign and no visual tampering was detected."
                threat_summary.append("Clean")
            else:
                threat_summary.append("Anomalous Indicators")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Do NOT scan this QR code. If found in a physical location, dispatch security to remove the fraudulent sticker. Block associated URLs or UPI addresses."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Proceed with caution. The payload contains unusual attributes requiring manual review."
        else:
            recommendation = "Safe to interact."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated Computer Vision tampering metrics with payment payload extraction."
        }

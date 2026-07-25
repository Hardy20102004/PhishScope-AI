class QRRiskScoringEngine:
    """
    Computes an overall risk score based on aggregated QR evidence.
    """
    
    @staticmethod
    def calculate(tampering: dict, payment: dict, visual: dict, url_risk_score: int = 0) -> dict:
        score = 0
        
        # Tampering Risk
        tampering_risk = 0
        if tampering.get("has_overlay_sticker"): tampering_risk += 60
        if tampering.get("has_logo_anomaly"): tampering_risk += 30
        score += tampering_risk
        
        # Payment Risk
        payment_risk = 0
        if payment.get("payment_network") != "None":
            # Just being a payment QR isn't inherently risky, but combined with tampering it is
            if tampering_risk > 0:
                payment_risk += 40
        score += payment_risk
        
        # URL Risk
        score += url_risk_score
        
        # Normalize
        score = min(score, 100)
        
        if score >= 80:
            threat_severity = "CRITICAL"
        elif score >= 60:
            threat_severity = "HIGH"
        elif score >= 30:
            threat_severity = "MEDIUM"
        else:
            threat_severity = "LOW"
            
        return {
            "overall_risk_score": score,
            "threat_severity": threat_severity,
            "tampering_risk": min(tampering_risk, 60),
            "payment_risk": min(payment_risk, 40),
            "url_risk": url_risk_score
        }

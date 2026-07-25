class WebsiteRiskScoringEngine:
    """
    Computes an overall risk score based on aggregated website evidence.
    """
    
    @staticmethod
    def calculate(html: dict, js: list, forms: list, cookies: dict, security: dict, visual: dict) -> dict:
        score = 0
        confidence = 100
        
        # Code Risk
        code_risk = 0
        if html.get("has_hidden_elements"): code_risk += 10
        if html.get("embedded_credentials"): code_risk += 30
        
        for script in js:
            if script.get("is_obfuscated"): code_risk += 15
            if script.get("uses_suspicious_apis"): code_risk += 10
            
        score += min(code_risk, 40)
        
        # Form Risk
        form_risk = 0
        for form in forms:
            if form.get("is_login") and not security.get("strict_transport_security"):
                form_risk += 30 # Login without HSTS/HTTPS
            if form.get("requests_personal_info"):
                form_risk += 10
        score += min(form_risk, 40)
        
        # Infrastructure/Security Risk
        infra_risk = 0
        if not security.get("content_security_policy"): infra_risk += 10
        if not security.get("x_frame_options"): infra_risk += 10
        if cookies.get("insecure_count", 0) > 0: infra_risk += 15
        score += min(infra_risk, 35)
        
        # Visual Risk
        visual_risk = 0
        if visual.get("impersonates_brand"):
            visual_risk += 50
        score += min(visual_risk, 50)
        
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
            "confidence": confidence,
            "threat_severity": threat_severity,
            "code_risk": min(code_risk, 40),
            "form_risk": min(form_risk, 40),
            "infrastructure_risk": min(infra_risk, 35),
            "visual_risk": min(visual_risk, 50)
        }

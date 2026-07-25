import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WebsiteAIIntegration:
    """
    Integrates Website Intelligence with PHOENIX AI Brain to generate explainable risk narratives.
    """
    
    @staticmethod
    async def generate_narrative(url: str, html: dict, js: list, forms: list, security: dict, visual: dict, risk: dict) -> Dict[str, str]:
        """
        Generates a human-readable threat narrative based on the collected website evidence.
        """
        
        narrative = f"Investigation of the website at {url} yields a {risk.get('threat_severity')} threat level with a score of {risk.get('overall_risk_score')}/100. "
        
        threat_summary = []
        
        # Visual & Brand
        if visual.get("impersonates_brand"):
            brand = visual.get("brand_name", "a known brand")
            narrative += f"Visual analysis indicates high similarity to {brand}, strongly suggesting a credential harvesting or phishing portal. "
            threat_summary.append("Brand Impersonation")
            if visual.get("is_fake_login"):
                threat_summary.append("Fake Login Portal")
                
        # Forms
        for form in forms:
            if form.get("is_login") and not security.get("strict_transport_security"):
                narrative += "A login form was detected on a page lacking Strict-Transport-Security (HSTS), increasing the risk of credential interception. "
                threat_summary.append("Insecure Login Form")
                break
                
        # Code/JS
        obfuscated_js = any(script.get("is_obfuscated") for script in js)
        if obfuscated_js:
            narrative += "Highly obfuscated JavaScript was detected, a technique commonly used to hide malicious payloads or tracking mechanisms. "
            threat_summary.append("Obfuscated Code")
            
        if html.get("has_hidden_elements"):
            narrative += "Hidden DOM elements were found, which may be used for clickjacking or evading automated scanners. "
            threat_summary.append("Hidden DOM Elements")
            
        if not threat_summary:
            if risk.get("overall_risk_score", 0) < 30:
                narrative += "The website behaves according to standard web practices with no significant malicious indicators."
                threat_summary.append("Clean")
            else:
                threat_summary.append("Multiple Minor Indicators")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Immediately block interactions with this website. Investigate any endpoints that communicated with it."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Enforce strong isolation (e.g., Remote Browser Isolation) if access is necessary."
        else:
            recommendation = "No immediate action required."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated DOM structure, JS execution context, visual appearance, and security headers."
        }

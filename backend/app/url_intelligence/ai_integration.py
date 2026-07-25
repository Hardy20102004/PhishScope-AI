import logging
from typing import Dict

# Assuming integration with existing AI modules, we'll mock the LLM call for this implementation
# In a real environment, this would call app.services.ai_service or app.ai_brain.model_manager

logger = logging.getLogger(__name__)

class URLAIIntegration:
    """
    Integrates URL Intelligence with PHOENIX AI Brain to generate explainable risk narratives.
    """
    
    @staticmethod
    async def generate_narrative(url: str, intel: dict, brand: dict, infra: dict, risk: dict) -> Dict[str, str]:
        """
        Generates a human-readable threat narrative based on the collected evidence.
        """
        
        narrative = f"Investigation of {url} indicates a {risk.get('threat_severity')} threat level with a score of {risk.get('overall_risk_score')}/100. "
        
        threat_summary = []
        
        # Evidence Synthesis
        if brand.get("is_typosquat"):
            target = brand.get("typosquat_target", "a known brand")
            narrative += f"The domain appears to be typosquatting {target}, presenting a severe brand impersonation risk. "
            threat_summary.append("Brand Impersonation (Typosquatting)")
            
        if brand.get("is_homograph"):
            narrative += "A homograph attack was detected in the domain name, likely intended to deceive users visually. "
            threat_summary.append("Visual Deception (Homograph)")
            
        if intel.get("credential_pattern"):
            narrative += "The URL contains embedded credentials or patterns designed to bypass standard parsing. "
            threat_summary.append("Credential Pattern Detected")
            
        if intel.get("suspicious_keywords_found"):
            kw = ", ".join(intel.get("suspicious_keywords_found"))
            narrative += f"Suspicious keywords ({kw}) frequently used in phishing were identified. "
            threat_summary.append("Phishing Keywords")
            
        certs = infra.get("certificates", [])
        if not certs:
            narrative += "No valid TLS certificate was found, indicating a lack of secure communication infrastructure. "
            threat_summary.append("Missing TLS Certificate")
        else:
            for cert in certs:
                if not cert.get("is_valid"):
                    narrative += "The associated TLS certificate is invalid or improperly configured. "
                    threat_summary.append("Invalid Certificate")
                    break
                    
        if risk.get("overall_risk_score", 0) < 30:
            narrative += "No significant malicious indicators were found during this investigation."
            if not threat_summary:
                threat_summary.append("Clean")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Block access to this URL immediately and investigate potential internal exposure."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Monitor traffic to this domain and warn users of potential risks."
        else:
            recommendation = "No immediate action required, but continue standard logging."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated evidence from DNS, certificate transparency, and visual brand checks."
        }

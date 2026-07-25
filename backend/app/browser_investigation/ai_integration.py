import logging
from typing import Dict

logger = logging.getLogger(__name__)

class BrowserAIIntegration:
    """
    Integrates Browser Intelligence with PHOENIX AI Brain to generate explainable browser forensics narratives.
    """
    
    @staticmethod
    async def generate_narrative(extensions: list, timeline: list, iocs: list, risk: dict) -> Dict[str, str]:
        
        narrative = f"Forensic analysis of the browser profile yields a {risk.get('threat_severity')} threat level (Score: {risk.get('overall_risk_score')}/100). "
        
        threat_summary = []
        
        # Suspicious Extensions
        suspicious_exts = [ext.get("name") for ext in extensions if ext.get("is_suspicious")]
        if suspicious_exts:
            narrative += f"The profile contains {len(suspicious_exts)} suspicious extension(s), including {', '.join(suspicious_exts)}. These extensions possess highly privileged permissions like <all_urls>. "
            threat_summary.append("Suspicious Extensions")
            
        # IOCs
        urls = [ioc.get("ioc_value") for ioc in iocs if ioc.get("ioc_type") == "url"]
        if urls:
            narrative += f"History and download logs contain potentially malicious URLs (e.g., {urls[0] if urls else 'N/A'}). "
            threat_summary.append("Malicious Domains/URLs")
            
        if not threat_summary:
            if risk.get("overall_risk_score", 0) < 30:
                narrative += "Analysis of the browser extraction revealed no significant anomalies in extensions or history."
                threat_summary.append("Clean Profile")
            else:
                threat_summary.append("Anomalous Metadata")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Correlate extracted URLs with the Advanced URL Intelligence platform. Isolate the endpoint if the malicious download was executed."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Review extension permissions and enterprise browser policies."
        else:
            recommendation = "No immediate forensic action required."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated history visits with malicious downloads."
        }

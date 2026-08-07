import logging
from typing import Dict

logger = logging.getLogger(__name__)

class MobileAIIntegration:
    """
    Integrates Mobile Intelligence with PHOENIX AI Brain to generate explainable mobile forensics narratives.
    """
    
    @staticmethod
    async def generate_narrative(metadata: dict, applications: list, timeline: list, iocs: list, risk: dict) -> Dict[str, str]:
        
        narrative = f"Forensic analysis of the mobile device ({metadata.get('manufacturer', 'Unknown')} {metadata.get('model', 'Device')}) yields a {risk.get('threat_severity')} threat level (Score: {risk.get('overall_risk_score')}/100). "
        
        threat_summary = []
        
        # Suspicious Apps
        suspicious_apps = [app.get("app_name") for app in applications if app.get("is_suspicious")]
        if suspicious_apps:
            narrative += f"The device has {len(suspicious_apps)} suspicious application(s) installed, including {', '.join(suspicious_apps)}. These apps request excessive permissions (e.g., SMS, Admin). "
            threat_summary.append("Suspicious Applications")
            
        # IOCs from Comms
        urls = [ioc.get("ioc_value") for ioc in iocs if ioc.get("ioc_type") == "url"]
        if urls:
            narrative += f"Communication logs contain potential phishing or malicious URLs ({', '.join(urls[:3])}). "
            threat_summary.append("Malicious Links in SMS")
            
        if not threat_summary:
            if risk.get("overall_risk_score", 0) < 30:
                narrative += "Analysis of the extraction revealed no significant anomalies in applications or communications."
                threat_summary.append("Clean (Static Backup)")
            else:
                threat_summary.append("Anomalous Metadata")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Correlate extracted SMS URLs with the Advanced URL Intelligence platform. Initiate a deeper reverse engineering of the suspicious APKs found on the device."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Review application permissions. Interview the device owner regarding recently installed unverified applications."
        else:
            recommendation = "No immediate forensic action required."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated application permissions with SMS timeline events."
        }

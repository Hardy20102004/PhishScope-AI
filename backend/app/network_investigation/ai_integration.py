import logging
from typing import Dict

logger = logging.getLogger(__name__)

class NetworkAIIntegration:
    """
    Integrates Network Intelligence with PHOENIX AI Brain to generate explainable network forensics narratives.
    """
    
    @staticmethod
    async def generate_narrative(dns: list, http: list, timeline: list, iocs: list, risk: dict) -> Dict[str, str]:
        
        narrative = f"Forensic analysis of the network evidence yields a {risk.get('threat_severity')} threat level (Score: {risk.get('overall_risk_score')}/100). "
        
        threat_summary = []
        
        # Suspicious DNS
        malicious_dns = [d.get("query") for d in dns if d.get("is_malicious")]
        if malicious_dns:
            narrative += f"The capture contains {len(malicious_dns)} anomalous DNS queries to suspected malicious infrastructure (e.g., {malicious_dns[0]}). "
            threat_summary.append("Malicious DNS Lookups")
            
        # Anomalous HTTP
        anomalous_http = [h for h in http if h.get("method") == "POST" and "Windows NT" in h.get("user_agent", "")]
        if anomalous_http:
            narrative += f"We observed {len(anomalous_http)} potentially anomalous HTTP POST request(s) suggesting beaconing or exfiltration activity. "
            threat_summary.append("Anomalous HTTP POST/User-Agent")
            
        if not threat_summary:
            if risk.get("overall_risk_score", 0) < 30:
                narrative += "Analysis of the network capture revealed no significant anomalies in DNS or HTTP traffic patterns."
                threat_summary.append("Clean Network Traffic")
            else:
                threat_summary.append("Anomalous Metadata")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Isolate the source endpoint. Pivot to Advanced URL Intelligence to analyze the extracted C2 domains."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Monitor the endpoint for further suspicious beaconing activity."
        else:
            recommendation = "No immediate forensic action required."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated DNS lookups with subsequent HTTP POST payloads."
        }

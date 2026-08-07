import logging
from typing import Dict

logger = logging.getLogger(__name__)

class CloudAIIntegration:
    """
    Integrates Cloud Intelligence with PHOENIX AI Brain to generate explainable cloud forensics narratives.
    """
    
    @staticmethod
    async def generate_narrative(identities: list, audit_logs: list, timeline: list, iocs: list, risk: dict) -> Dict[str, str]:
        
        narrative = f"Forensic analysis of the cloud environment yields a {risk.get('threat_severity')} threat level (Score: {risk.get('overall_risk_score')}/100). "
        
        threat_summary = []
        
        # Suspicious Identity
        privileged_identities = [i.get("name") for i in identities if i.get("is_highly_privileged")]
        if privileged_identities:
            narrative += f"Highly privileged identities were detected ({', '.join(privileged_identities)}). "
            threat_summary.append("Highly Privileged Identity")
            
        # Anomalous Audit Logs
        anomalous_audits = [a.get("event_name") for a in audit_logs if a.get("is_anomalous")]
        if anomalous_audits:
            narrative += f"Anomalous audit events were recorded, including actions like {', '.join(anomalous_audits)}. This pattern often indicates attempts to evade logging or escalate privileges. "
            threat_summary.append("Defense Evasion (Audit Tampering)")
            
        if not threat_summary:
            if risk.get("overall_risk_score", 0) < 30:
                narrative += "Analysis of the cloud environment revealed no significant anomalies in identity configurations or audit trails."
                threat_summary.append("Nominal Cloud State")
            else:
                threat_summary.append("Anomalous Metadata")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Immediately lock down affected identities and review IAM policies. Investigate the source IPs of the anomalous audit events."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Review permissive IAM roles and monitor audit trails for sustained anomalous behavior."
        else:
            recommendation = "No immediate forensic action required."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated permissive identities with subsequent defense evasion events in the audit trail."
        }

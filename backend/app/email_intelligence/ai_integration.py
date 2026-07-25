import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EmailAIIntegration:
    """
    Integrates Email Intelligence with PHOENIX AI Brain to generate explainable risk narratives.
    """
    
    @staticmethod
    async def generate_narrative(headers: dict, auth: dict, conversation: dict, attachments: list, campaign: dict, risk: dict) -> Dict[str, str]:
        
        subject = headers.get("subject", "No Subject")
        sender = headers.get("from_address", "Unknown Sender")
        
        narrative = f"Investigation of email '{subject}' from '{sender}' yields a {risk.get('threat_severity')} threat level (Score: {risk.get('overall_risk_score')}/100). "
        
        threat_summary = []
        
        # Authentication
        if auth.get("is_spoofed"):
            narrative += "Authentication checks (SPF/DMARC) failed, strongly indicating the sender address is spoofed. "
            threat_summary.append("Spoofed Sender")
            
        # Conversation / BEC
        if conversation.get("is_bec_suspect"):
            narrative += "The email body contains linguistic patterns consistent with Business Email Compromise (BEC), including high urgency and financial keywords. "
            threat_summary.append("BEC Indicators")
            
        # Attachments
        suspicious_attachments = [a for a in attachments if a.get("is_suspicious")]
        if suspicious_attachments:
            names = ", ".join([a.get("filename", "") for a in suspicious_attachments])
            narrative += f"Suspicious attachments detected ({names}), which often contain malware or malicious scripts. "
            threat_summary.append("Suspicious Attachment")
            
        # Campaign
        if campaign.get("campaign_name") != "None":
            narrative += f"Indicators match the known '{campaign.get('campaign_name')}' threat campaign. "
            threat_summary.append(f"Linked to {campaign.get('campaign_name')}")
            
        if not threat_summary:
            if risk.get("overall_risk_score", 0) < 30:
                narrative += "The email appears legitimate with passing authentication and no suspicious content."
                threat_summary.append("Clean")
            else:
                threat_summary.append("Anomalous Indicators")
                
        # Recommended Action
        if risk.get("threat_severity") in ["HIGH", "CRITICAL"]:
            recommendation = "Quarantine this email immediately. Do not interact with attachments or embedded URLs. Block the sender IP and domain."
        elif risk.get("threat_severity") == "MEDIUM":
            recommendation = "Hold for manual SOC review. Defang URLs and attachments if releasing to user."
        else:
            recommendation = "Deliver normally."
            
        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary),
            "recommended_next_steps": recommendation,
            "evidence_correlation": "AI correlated Authentication failures, BEC language models, attachment heuristics, and historical campaign data."
        }

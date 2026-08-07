class EmailRiskScoringEngine:
    """
    Computes an overall risk score based on aggregated email evidence.
    """
    
    @staticmethod
    def calculate(auth: dict, conversation: dict, attachments: list, campaign: dict) -> dict:
        score = 0
        
        # Auth Risk
        auth_risk = 0
        if auth.get("is_spoofed"):
            auth_risk += 40
        score += auth_risk
        
        # Conversation / BEC Risk
        bec_risk = 0
        if conversation.get("is_bec_suspect"):
            bec_risk += 30
        score += bec_risk
        
        # Attachment Risk
        att_risk = 0
        if any(a.get("is_suspicious") for a in attachments):
            att_risk += 40
        score += att_risk
        
        # Campaign Risk
        if campaign.get("campaign_name") != "None":
            score += 20
            
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
            "authentication_risk": auth_risk,
            "bec_risk": bec_risk,
            "attachment_risk": min(att_risk, 40)
        }

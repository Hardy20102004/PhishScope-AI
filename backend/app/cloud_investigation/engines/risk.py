from typing import Dict, Any, List

class RiskAssessmentEngine:
    @staticmethod
    def calculate(assets: List[Dict[str, Any]], identities: List[Dict[str, Any]], configs: List[Dict[str, Any]], audits: List[Dict[str, Any]]) -> dict:
        score = 0
        
        asset_risk = sum([10 for a in assets if a.get("is_public")])
        identity_risk = sum([20 for i in identities if i.get("is_highly_privileged")])
        config_risk = sum([30 for c in configs if c.get("is_misconfigured")])
        audit_risk = sum([50 for a in audits if a.get("is_anomalous")])
        
        score = asset_risk + identity_risk + config_risk + audit_risk
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
            "asset_risk": min(asset_risk, 100),
            "identity_risk": min(identity_risk, 100),
            "config_risk": min(config_risk, 100),
            "audit_risk": min(audit_risk, 100)
        }

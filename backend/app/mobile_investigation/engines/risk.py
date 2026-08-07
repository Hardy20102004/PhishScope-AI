from typing import Any, Dict, List


class RiskAssessmentEngine:
    """
    Computes an overall risk score based on mobile forensic indicators.
    """
    
    @staticmethod
    def calculate(applications: List[Dict[str, Any]], iocs: List[Dict[str, str]]) -> dict:
        score = 0
        
        # App Risk
        app_risk = sum([30 for app in applications if app.get("is_suspicious")])
        score += app_risk
        
        # IOC Risk
        ioc_risk = 0
        for ioc in iocs:
            if ioc.get("ioc_type") == "url":
                ioc_risk += 15 # Treat extracted URLs as moderate risk pending reputation check
                
        score += ioc_risk
        
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
            "application_risk": min(app_risk, 50),
            "ioc_risk": min(ioc_risk, 50)
        }

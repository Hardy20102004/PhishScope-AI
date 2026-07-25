from typing import Dict, Any, List

class RiskAssessmentEngine:
    """
    Computes an overall risk score based on browser artifacts.
    """
    
    @staticmethod
    def calculate(extensions: List[Dict[str, Any]], downloads: List[Dict[str, Any]]) -> dict:
        score = 0
        
        # Extension Risk
        ext_risk = sum([40 for ext in extensions if ext.get("is_suspicious")])
        score += ext_risk
        
        # Download Risk
        dl_risk = sum([50 for dl in downloads if dl.get("is_malicious")])
        score += dl_risk
        
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
            "extension_risk": min(ext_risk, 50),
            "download_risk": min(dl_risk, 50)
        }

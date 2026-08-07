from typing import Any, Dict, List


class RiskAssessmentEngine:
    @staticmethod
    def calculate(dns: List[Dict[str, Any]], http: List[Dict[str, Any]]) -> dict:
        score = 0
        
        dns_risk = sum([40 for d in dns if d.get("is_malicious")])
        score += dns_risk
        
        http_risk = 0
        for h in http:
            if h.get("method") == "POST" and "Windows NT" in h.get("user_agent", ""):
                http_risk += 10 # Slight heuristic anomaly depending on context, mock logic
        score += http_risk
        
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
            "dns_risk": min(dns_risk, 50),
            "http_risk": min(http_risk, 50)
        }

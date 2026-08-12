from typing import Any, Dict, List


class RiskAssessmentEngine:
    """
    Computes an overall risk score based on mobile forensic indicators.
    """
    
    @staticmethod
    def calculate(applications: List[Dict[str, Any]], iocs: List[Dict[str, str]], parsed_data: Dict[str, Any] = None) -> dict:
        score = 0
        payload_type = (parsed_data or {}).get("payload_type", "")
        
        if payload_type == "payment_upi_legitimate":
            score = 15
            app_risk = 5
            ioc_risk = 10
            threat_severity = "LOW"
            infra_risk = "Low"
            brand_risk = "Clean (Valid VPA Handle)"
            confidence = 95
        elif payload_type == "payment_upi_scam":
            score = 85
            app_risk = 40
            ioc_risk = 45
            threat_severity = "HIGH"
            infra_risk = "High"
            brand_risk = "High (VPA Fraud / Deceptive Note)"
            confidence = 90
        elif payload_type == "trojan_apk":
            score = 95
            app_risk = 50
            ioc_risk = 45
            threat_severity = "CRITICAL"
            infra_risk = "Critical"
            brand_risk = "High (Trojan Dropper)"
            confidence = 98
        elif payload_type == "banking_phishing":
            score = 90
            app_risk = 45
            ioc_risk = 45
            threat_severity = "CRITICAL"
            infra_risk = "Critical"
            brand_risk = "High (Bank Impersonation)"
            confidence = 95
        else:
            # Dynamic calculation based on suspicious apps and IOCs
            app_risk = sum([30 for app in applications if app.get("is_suspicious")])
            ioc_risk = 0
            for ioc in iocs:
                if ioc.get("ioc_type") in ["url", "vpa"]:
                    ioc_risk += 25
                elif ioc.get("ioc_type") == "phone_number":
                    ioc_risk += 10
            
            score = app_risk + ioc_risk
            if not score:
                score = 15
            
            score = min(max(score, 15), 98)
            if score >= 85:
                threat_severity = "CRITICAL"
                infra_risk = "High"
                brand_risk = "Moderate"
            elif score >= 65:
                threat_severity = "HIGH"
                infra_risk = "Moderate"
                brand_risk = "Moderate"
            elif score >= 35:
                threat_severity = "MEDIUM"
                infra_risk = "Low"
                brand_risk = "Low"
            else:
                threat_severity = "LOW"
                infra_risk = "Low"
                brand_risk = "Clean"
            confidence = 90
            
        return {
            "overall_risk_score": score,
            "threat_severity": threat_severity,
            "confidence": confidence,
            "infrastructure_risk": infra_risk,
            "brand_risk": brand_risk,
            "application_risk": min(app_risk, 50),
            "ioc_risk": min(ioc_risk, 50)
        }



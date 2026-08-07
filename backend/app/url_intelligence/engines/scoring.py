class RiskScoringEngine:
    """
    Computes an overall risk score based on aggregated evidence.
    """
    
    @staticmethod
    def calculate(intel: dict, brand: dict, infra: dict) -> dict:
        score = 0
        confidence = 100
        threat_severity = "LOW"
        
        # 1. URL Intelligence Risk
        if intel.get("suspicious_keywords_found"):
            score += 20
        if intel.get("credential_pattern"):
            score += 40
        if intel.get("entropy", 0) > 4.5: # High entropy
            score += 10
            
        # 2. Brand Risk
        if brand.get("is_typosquat"):
            score += 50
        if brand.get("is_homograph"):
            score += 60
            
        # 3. Infrastructure Risk
        certs = infra.get("certificates", [])
        if not certs:
            score += 20
        else:
            for cert in certs:
                if not cert.get("is_valid"):
                    score += 30
                    
        # Normalize score
        score = min(score, 100)
        
        if score >= 80:
            threat_severity = "CRITICAL"
        elif score >= 60:
            threat_severity = "HIGH"
        elif score >= 30:
            threat_severity = "MEDIUM"
            
        # Calculate Evidence Quality based on what data we were able to fetch
        evidence_quality = "HIGH"
        if not infra.get("ips"):
            confidence -= 20
            evidence_quality = "MEDIUM"
            
        return {
            "overall_risk_score": score,
            "confidence": confidence,
            "threat_severity": threat_severity,
            "evidence_quality": evidence_quality,
            "infrastructure_risk": min(score, 40),
            "brand_risk": min(score, 60) if brand.get("is_typosquat") else 0
        }

class RiskScoringEngine:
    """
    Computes an overall risk score based on aggregated evidence.
    
    Fixed (v2):
    - BUG-005: brand_risk now correctly reflects only the brand-specific 
      contribution, not the total score. Previously: min(total_score, 60) 
      which was misleading when infrastructure/URL also contributed.
    """
    
    @staticmethod
    def calculate(intel: dict, brand: dict, infra: dict) -> dict:
        score = 0
        confidence = 100
        threat_severity = "LOW"
        
        # --- Score components tracked separately for accurate attribution ---
        url_risk_score = 0
        brand_risk_score = 0
        infra_risk_score = 0
        
        # 1. URL Intelligence Risk
        if intel.get("suspicious_keywords_found"):
            url_risk_score += 20
        if intel.get("credential_pattern"):
            url_risk_score += 40
        if intel.get("entropy", 0) > 4.5:  # High entropy indicates obfuscation
            url_risk_score += 10
        if intel.get("nested_redirect_parameters"):
            url_risk_score += 10  # Open redirect potential
            
        # 2. Brand Risk (tracked separately — BUG-005 fix)
        if brand.get("is_typosquat"):
            brand_risk_score += 50
        if brand.get("is_homograph"):
            brand_risk_score += 60
            
        # 3. Infrastructure Risk (tracked separately)
        certs = infra.get("certificates", [])
        if not certs:
            infra_risk_score += 20
        else:
            for cert in certs:
                if not cert.get("is_valid"):
                    infra_risk_score += 30
        
        # Cap each component reasonably
        url_risk_score = min(url_risk_score, 70)
        brand_risk_score = min(brand_risk_score, 80)
        infra_risk_score = min(infra_risk_score, 40)
        
        # Total score — weighted combination
        score = min(url_risk_score + brand_risk_score + infra_risk_score, 100)
        
        # Severity thresholds
        if score >= 80:
            threat_severity = "CRITICAL"
        elif score >= 60:
            threat_severity = "HIGH"
        elif score >= 30:
            threat_severity = "MEDIUM"
        else:
            threat_severity = "LOW"
        
        # Evidence quality — affected by what data we could actually fetch
        if not infra.get("ips"):
            confidence -= 20
            evidence_quality = "MEDIUM"
        elif not infra.get("nameservers"):
            confidence -= 10
            evidence_quality = "MEDIUM"
        else:
            evidence_quality = "HIGH"
        
        confidence = max(confidence, 0)
        
        return {
            "overall_risk_score": score,
            "confidence": confidence,
            "threat_severity": threat_severity,
            "evidence_quality": evidence_quality,
            # BUG-005 FIX: Each component now reports its own actual contribution
            "url_risk": url_risk_score,
            "brand_risk": brand_risk_score,
            "infrastructure_risk": infra_risk_score,
        }

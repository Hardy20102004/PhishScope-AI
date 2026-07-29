from typing import Dict, Any

class AlertPrioritizationEngine:
    """
    Calculates dynamic Risk and Priority scores based on asset criticality,
    threat severity, and evidence quality.
    """
    
    SEVERITY_WEIGHTS = {
        "LOW": 1.0,
        "MEDIUM": 3.0,
        "HIGH": 6.0,
        "CRITICAL": 10.0
    }

    @classmethod
    def calculate_scores(cls, alert_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculates priority_score, risk_score, and confidence for a given alert.
        """
        severity_val = cls.SEVERITY_WEIGHTS.get(alert_data.get("severity", "MEDIUM"), 3.0)
        
        # Calculate Risk Score (impact * probability)
        # In a real scenario, this would lookup Asset Criticality from a CMDB
        asset_criticality = 5.0 # Mock average criticality
        risk_score = min(100.0, severity_val * asset_criticality * 2.0)
        
        # Calculate Evidence Quality (Confidence)
        evidence_count = len(alert_data.get("evidence", []))
        confidence = min(100.0, 50.0 + (evidence_count * 10.0))
        
        # Calculate Final Priority Score
        priority_score = min(100.0, (risk_score * 0.7) + (confidence * 0.3))
        
        return {
            "priority_score": round(priority_score, 2),
            "risk_score": round(risk_score, 2),
            "confidence": round(confidence, 2)
        }

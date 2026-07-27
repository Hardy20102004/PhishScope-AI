from typing import List
from app.models.threat_intel import IndicatorCorrelation, CorrelationEvidence

class ConfidenceEngine:
    """
    Calculates confidence scores for IOC relationships.
    """

    @staticmethod
    def calculate_confidence(relationship: IndicatorCorrelation, evidence_list: List[CorrelationEvidence]) -> float:
        """
        Calculates confidence score (0.0 to 1.0) based on evidence.
        """
        if not evidence_list:
            return 0.1 # Very low confidence if no evidence
            
        base_score = 0.0
        
        # 1. Evidence Quantity (Max 0.3)
        quantity_score = min(len(evidence_list) * 0.1, 0.3)
        base_score += quantity_score
        
        # 2. Evidence Quality (Max 0.5)
        # Different sources have different weights
        quality_score = 0.0
        for evidence in evidence_list:
            if evidence.source_system == "Internal Knowledge Graph":
                quality_score += 0.2
            elif evidence.source_system in ["VirusTotal", "CrowdStrike"]:
                quality_score += 0.3
            else:
                quality_score += 0.1
                
        base_score += min(quality_score, 0.5)
        
        # 3. Relationship Strength (Max 0.2)
        if relationship.correlation_type == "Exact Match":
            base_score += 0.2
        elif relationship.correlation_type == "Infrastructure Sharing":
            base_score += 0.1
            
        return min(base_score, 1.0)

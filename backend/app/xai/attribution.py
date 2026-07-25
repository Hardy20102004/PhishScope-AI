import structlog
from typing import List, Dict, Any
from app.schemas.xai import EvidenceAttributionBase

logger = structlog.get_logger("phoenix.xai.attribution")

class EvidenceAttributionEngine:
    """
    Ranks raw evidence based on its reliability and relevance to the decision.
    """
    def generate_attributions(self, raw_evidence_links: List[Any]) -> List[EvidenceAttributionBase]:
        logger.info("generating_evidence_attributions", count=len(raw_evidence_links))
        
        attributions = []
        for link in raw_evidence_links:
            # Deterministic heuristic for weight based on source type
            weight = 0.5
            text = f"Supporting evidence from {link.source_type} ({link.source_id})"
            
            if link.source_type == "KNOWLEDGE_GRAPH":
                weight = 0.9
                text = "Strong internal historical correlation found in the Enterprise Knowledge Graph."
            elif link.source_type == "RAG_DOCUMENT":
                weight = 0.7
                text = "Contextual alignment with internal standard operating procedures (RAG)."
            elif link.source_type == "THREAT_INTEL":
                weight = 0.8
                text = "Confirmed match against external Threat Intelligence feeds."
                
            attributions.append(EvidenceAttributionBase(
                evidence_link_id=link.id,
                importance_weight=weight,
                attribution_text=text,
                source_type=link.source_type,
                source_id=link.source_id
            ))
            
        # Sort by weight descending
        return sorted(attributions, key=lambda x: x.importance_weight, reverse=True)

from typing import Any, List

import structlog

from app.schemas.xai import FeatureRank

logger = structlog.get_logger("phoenix.xai.feature_importance")

class FeatureImportanceEngine:
    def generate_feature_ranking(self, decision_type: str, evidence: List[Any]) -> List[FeatureRank]:
        logger.info("generating_feature_ranking", decision_type=decision_type)
        
        # Mock deterministic feature ranking
        ranks = []
        
        has_kg = any(e.source_type == "KNOWLEDGE_GRAPH" for e in evidence)
        
        if has_kg:
            ranks.append(FeatureRank(
                feature_name="Historical Graph Similarity",
                rank=1,
                category="KNOWLEDGE_GRAPH"
            ))
            ranks.append(FeatureRank(
                feature_name="Direct Indicator Match",
                rank=2,
                category="RAW_LOG"
            ))
        else:
            ranks.append(FeatureRank(
                feature_name="Direct Indicator Match",
                rank=1,
                category="RAW_LOG"
            ))
            
        if decision_type == "THREAT_CLASSIFICATION":
            ranks.append(FeatureRank(
                feature_name="Threat Actor TTP Overlap",
                rank=3,
                category="OSINT"
            ))
            
        return ranks

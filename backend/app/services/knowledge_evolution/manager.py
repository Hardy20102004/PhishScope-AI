from sqlalchemy.orm import Session

from app.services.knowledge_evolution.ontology_management import OntologyManagementEngine
from app.services.knowledge_evolution.relationship_discovery import RelationshipDiscoveryEngine
from app.services.knowledge_evolution.semantic_enrichment import SemanticEnrichmentEngine
from app.services.knowledge_evolution.knowledge_quality import KnowledgeQualityEngine
from app.services.knowledge_evolution.schema_recommendation import SchemaRecommendationEngine

class KnowledgeEvolutionManager:
    """
    Central orchestrator for the Knowledge Evolution Platform.
    """
    def __init__(self, db: Session):
        self.db = db
        self.ontology = OntologyManagementEngine(db)
        self.discovery = RelationshipDiscoveryEngine(db)
        self.enrichment = SemanticEnrichmentEngine(db)
        self.quality = KnowledgeQualityEngine(db)
        self.schema = SchemaRecommendationEngine(db)

    def get_overview_stats(self) -> dict:
        nodes = self.ontology.get_nodes()
        recommendations = self.schema.get_pending_recommendations()
        
        return {
            "total_ontology_nodes": len(nodes),
            "pending_recommendations": len(recommendations),
            "overall_quality_score": 88
        }

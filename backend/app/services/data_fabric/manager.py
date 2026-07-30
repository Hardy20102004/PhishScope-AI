from sqlalchemy.orm import Session

from app.services.data_fabric.metadata_catalog import MetadataCatalogEngine
from app.services.data_fabric.data_lineage import DataLineageEngine
from app.services.data_fabric.data_quality import DataQualityEngine
from app.services.data_fabric.knowledge_mesh import KnowledgeMeshEngine
from app.services.data_fabric.governance import GovernanceEngine
from app.services.data_fabric.semantic_relationships import SemanticRelationshipEngine

class SecurityDataFabricManager:
    """
    Central orchestrator for the Enterprise Security Data Fabric.
    """
    def __init__(self, db: Session):
        self.db = db
        self.metadata_catalog = MetadataCatalogEngine(db)
        self.data_lineage = DataLineageEngine(db)
        self.data_quality = DataQualityEngine(db)
        self.knowledge_mesh = KnowledgeMeshEngine(db)
        self.governance = GovernanceEngine(db)
        self.semantic_relationships = SemanticRelationshipEngine(db)

    def get_overview_stats(self) -> dict:
        # Mock overall platform statistics
        return {
            "total_metadata_nodes": 15420,
            "total_lineage_edges": 45030,
            "overall_quality_score": 92,
            "active_policies": 14
        }

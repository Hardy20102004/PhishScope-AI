from sqlalchemy.orm import Session
from app.reputation_engine.models import ReputationProfile
from app.knowledge_graph.managers import RelationshipManager
from loguru import logger

class RelationshipInfluenceEngine:
    """
    Adjusts reputation based on Knowledge Graph connectivity.
    (e.g., A domain hosted on a malicious IP inherits risk).
    """
    def __init__(self, db: Session):
        self.db = db
        self.rel_manager = RelationshipManager(db)

    def calculate_influence(self, profile: ReputationProfile) -> tuple[float, float]:
        """
        Calculates the risk/trust delta modifier based on a 1-hop neighborhood scan.
        """
        logger.info(f"Scanning KG relationships for influence on {profile.entity_id}")
        
        # In a real implementation:
        # relationships = self.rel_manager.get_relationships(profile.entity_id)
        # return aggregated_risk_influence, aggregated_trust_influence
        
        # Mocking the calculation
        inherited_risk = 5.0 # Flat bump if connected to bad infra
        inherited_trust = -2.0
        
        return inherited_risk, inherited_trust

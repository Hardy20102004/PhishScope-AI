from sqlalchemy.orm import Session
from app.attack_graph.models import ImpactAnalysis
from loguru import logger

class ImpactAnalysisEngine:
    """
    Calculates Centrality and Blast Radius for nodes to find critical infrastructure.
    """
    def __init__(self, db: Session):
        self.db = db

    def calculate_node_impact(self, entity_id: str) -> ImpactAnalysis:
        logger.info(f"Calculating impact metrics for {entity_id}")
        
        # Mock calculation. Real implementation would run PageRank or Betweenness Centrality
        # on the Knowledge Graph.
        impact = ImpactAnalysis(
            entity_id=entity_id,
            degree_centrality=0.85,
            betweenness_centrality=0.72,
            blast_radius=120
        )
        
        self.db.add(impact)
        self.db.commit()
        self.db.refresh(impact)
        return impact

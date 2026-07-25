from typing import Dict, List

import networkx as nx
import structlog
from sqlalchemy.orm import Session

from app.models.knowledge_graph import (
    EntityStatus,
    GraphEntity,
    GraphRelationship,
    RelationshipStatus,
)

logger = structlog.get_logger("phoenix.kg.analytics")

class GraphAnalyticsEngine:
    def __init__(self, db: Session):
        self.db = db

    def _build_nx_graph(self) -> nx.DiGraph:
        """Loads the active graph from SQLite into a NetworkX Directed Graph."""
        G = nx.DiGraph()
        
        entities = self.db.query(GraphEntity).filter_by(status=EntityStatus.ACTIVE).all()
        for e in entities:
            G.add_node(e.id, type=e.entity_type, name=e.name)
            
        rels = self.db.query(GraphRelationship).filter_by(status=RelationshipStatus.ACTIVE).all()
        for r in rels:
            G.add_edge(r.source_id, r.target_id, type=r.relationship_type, weight=r.weight)
            
        return G

    def calculate_centrality(self) -> Dict[str, float]:
        """Calculates Degree Centrality to find highly connected entities (e.g. core C2 servers)."""
        logger.info("calculating_degree_centrality")
        G = self._build_nx_graph()
        if len(G) == 0:
            return {}
        return nx.degree_centrality(G)

    def detect_communities(self) -> List[List[str]]:
        """
        Uses greedy modularity optimization to find clusters of threat activity.
        (Requires undirected graph for standard modularity)
        """
        logger.info("detecting_graph_communities")
        G = self._build_nx_graph().to_undirected()
        if len(G) == 0:
            return []
            
        try:
            from networkx.algorithms.community import greedy_modularity_communities
            communities = greedy_modularity_communities(G)
            return [list(c) for c in communities]
        except Exception as e:
            logger.error("community_detection_failed", error=str(e))
            return []

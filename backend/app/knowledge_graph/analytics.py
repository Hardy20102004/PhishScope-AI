from typing import Dict, List, Any
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
    """
    Computes graph metrics and detects clusters.
    """
    def __init__(self, db: Session):
        self.db = db

    def _build_nx_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        
        entities = self.db.query(GraphEntity).filter_by(status=EntityStatus.ACTIVE).all()
        for e in entities:
            G.add_node(e.id, type=e.entity_type, name=e.name)
            
        rels = self.db.query(GraphRelationship).filter_by(status=RelationshipStatus.ACTIVE).all()
        for r in rels:
            G.add_edge(r.source_id, r.target_id, type=r.relationship_type, weight=r.weight, is_inferred=r.is_inferred)
            
        return G

    def calculate_centrality(self) -> List[Dict[str, Any]]:
        """Calculates Degree Centrality to find highly connected entities."""
        logger.info("calculating_degree_centrality")
        G = self._build_nx_graph()
        if len(G) == 0:
            return []
            
        centrality = nx.degree_centrality(G)
        # Sort and return top 10
        sorted_cent = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        results = []
        for node_id, score in sorted_cent:
            node_data = G.nodes[node_id]
            results.append({
                "entity_id": node_id,
                "name": node_data.get("name"),
                "type": node_data.get("type"),
                "centrality_score": score
            })
        return results

    def detect_threat_clusters(self) -> List[Dict[str, Any]]:
        """
        Uses greedy modularity optimization to find clusters of threat activity.
        """
        logger.info("detecting_threat_clusters")
        G = self._build_nx_graph().to_undirected()
        if len(G) == 0:
            return []
            
        try:
            from networkx.algorithms.community import greedy_modularity_communities
            communities = greedy_modularity_communities(G)
            
            clusters = []
            for i, comm in enumerate(communities):
                if len(comm) > 2: # Ignore trivial clusters
                    entities = [{"id": n, "name": G.nodes[n].get("name")} for n in comm]
                    clusters.append({
                        "cluster_id": f"cluster-{i}",
                        "size": len(comm),
                        "entities": entities
                    })
            return clusters
        except Exception as e:
            logger.error("community_detection_failed", error=str(e))
            return []

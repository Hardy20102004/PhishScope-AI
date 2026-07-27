from typing import List, Dict, Any, Optional
import networkx as nx
import structlog
from sqlalchemy.orm import Session

from app.models.knowledge_graph import (
    EntityStatus,
    GraphEntity,
    GraphRelationship,
    RelationshipStatus,
)
from app.knowledge_graph.analytics import GraphAnalyticsEngine

logger = structlog.get_logger("phoenix.kg.query")

class GraphQueryEngine:
    """
    Executes complex graph traversals and pattern searches.
    """
    def __init__(self, db: Session):
        self.db = db
        self.analytics = GraphAnalyticsEngine(db)

    def get_neighbors(self, entity_id: str, depth: int = 1) -> Dict[str, Any]:
        """
        Returns a subgraph centered around the given entity up to `depth` hops.
        Using NetworkX for simplicity in this prototype.
        """
        G = self.analytics._build_nx_graph().to_undirected()
        
        if entity_id not in G:
            return {"nodes": [], "edges": []}
            
        # Get nodes within 'depth' hops
        nodes_in_subgraph = nx.single_source_shortest_path_length(G, entity_id, cutoff=depth).keys()
        subgraph = G.subgraph(nodes_in_subgraph)
        
        # Serialize to JSON-friendly format
        nodes = []
        for n, data in subgraph.nodes(data=True):
            nodes.append({"id": n, "name": data.get("name"), "type": data.get("type")})
            
        edges = []
        for u, v, data in subgraph.edges(data=True):
            edges.append({"source": u, "target": v, "type": data.get("type"), "is_inferred": data.get("is_inferred", False)})
            
        return {"nodes": nodes, "edges": edges}

    def shortest_path(self, source_id: str, target_id: str) -> Dict[str, Any]:
        """
        Finds the shortest path between two entities.
        """
        G = self.analytics._build_nx_graph().to_undirected()
        
        if source_id not in G or target_id not in G:
            return {"nodes": [], "edges": [], "error": "Source or target not found in graph."}
            
        try:
            path = nx.shortest_path(G, source=source_id, target=target_id)
            subgraph = G.subgraph(path)
            
            nodes = []
            for n, data in subgraph.nodes(data=True):
                nodes.append({"id": n, "name": data.get("name"), "type": data.get("type")})
                
            edges = []
            for i in range(len(path)-1):
                u = path[i]
                v = path[i+1]
                edge_data = G.get_edge_data(u, v) or {}
                edges.append({"source": u, "target": v, "type": edge_data.get("type", "UNKNOWN")})
                
            return {"nodes": nodes, "edges": edges}
        except nx.NetworkXNoPath:
            return {"nodes": [], "edges": [], "error": "No path exists between these entities."}

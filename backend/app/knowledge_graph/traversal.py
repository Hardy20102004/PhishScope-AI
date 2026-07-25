import structlog
from typing import List, Dict, Any, Set
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.knowledge_graph import GraphEntity, GraphRelationship, EntityStatus, RelationshipStatus

logger = structlog.get_logger("phoenix.kg.traversal")

class TraversalEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_neighborhood(self, entity_id: str, depth: int = 1) -> Dict[str, List[Any]]:
        """
        Retrieves the subgraph surrounding an entity up to `depth` hops.
        Returns a dict with 'entities' and 'relationships'.
        """
        # For prototype SQLite, we do BFS in Python memory.
        # In a real DB like Neo4j or Postgres (with recursive CTE), we'd push this down.
        
        visited_nodes: Set[str] = set()
        visited_edges: Set[str] = set()
        nodes = []
        edges = []
        
        queue = [(entity_id, 0)]
        
        while queue:
            current_id, current_depth = queue.pop(0)
            
            if current_id in visited_nodes:
                continue
                
            entity = self.db.query(GraphEntity).filter_by(id=current_id, status=EntityStatus.ACTIVE).first()
            if not entity:
                continue
                
            visited_nodes.add(current_id)
            nodes.append(entity)
            
            if current_depth < depth:
                # Get outgoing
                outgoing = self.db.query(GraphRelationship).filter_by(source_id=current_id, status=RelationshipStatus.ACTIVE).all()
                for rel in outgoing:
                    if rel.id not in visited_edges:
                        visited_edges.add(rel.id)
                        edges.append(rel)
                        queue.append((rel.target_id, current_depth + 1))
                        
                # Get incoming
                incoming = self.db.query(GraphRelationship).filter_by(target_id=current_id, status=RelationshipStatus.ACTIVE).all()
                for rel in incoming:
                    if rel.id not in visited_edges:
                        visited_edges.add(rel.id)
                        edges.append(rel)
                        queue.append((rel.source_id, current_depth + 1))

        return {
            "entities": nodes,
            "relationships": edges
        }

from sqlalchemy.orm import Session
from app.knowledge_graph.managers import EntityManager, RelationshipManager
from app.attack_graph.schemas import GraphPayload, GraphNode, GraphLink
from loguru import logger

class AttackGraphBuilder:
    """
    Constructs a JSON-friendly subgraph payload by querying the Enterprise Knowledge Graph.
    """
    def __init__(self, db: Session):
        self.db = db
        self.entity_manager = EntityManager(db)
        self.rel_manager = RelationshipManager(db)

    def build_subgraph(self, seed_entity_id: str, depth: int = 2) -> GraphPayload:
        """
        Builds a graph starting from a seed entity, traversing relationships up to `depth` hops.
        In a real graph DB (Neo4j/Neptune), this is a single cypher/gremlin query.
        For our relational Knowledge Graph abstraction, we simulate the traversal.
        """
        logger.info(f"Building attack graph from seed {seed_entity_id} with depth {depth}")
        
        # Mocking the graph retrieval since true recursive traversal on SQL is complex without CTEs
        # We will return a structured payload mimicking what a true graph query would return.
        
        # In a real implementation:
        # nodes, edges = self.rel_manager.traverse(seed_entity_id, max_depth=depth)
        
        # Mock data structure to satisfy the frontend needs
        return GraphPayload(
            nodes=[
                GraphNode(id="apt29", label="APT29", type="Threat Actor"),
                GraphNode(id="op_ghost", label="Op Ghost Hunt", type="Campaign"),
                GraphNode(id="ip1", label="192.168.1.50", type="Infrastructure"),
                GraphNode(id="victim1", label="Defense Corp", type="Victim"),
            ],
            links=[
                GraphLink(source="apt29", target="op_ghost", type="ATTRIBUTED_TO"),
                GraphLink(source="op_ghost", target="ip1", type="USES"),
                GraphLink(source="ip1", target="victim1", type="TARGETS")
            ]
        )

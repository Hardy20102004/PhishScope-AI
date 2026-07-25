import structlog
from sqlalchemy.orm import Session

from app.knowledge_graph.managers import EntityManager, RelationshipManager
from app.models.knowledge_graph import EntityStatus, GraphEntity, GraphRelationship

logger = structlog.get_logger("phoenix.kg.inference")

class InferenceEngine:
    def __init__(self, db: Session):
        self.db = db
        self.entity_manager = EntityManager(db)
        self.rel_manager = RelationshipManager(db)

    def infer_shared_infrastructure(self):
        """
        Example Heuristic: If two domains resolve to the exact same IP Address, 
        create a 'RELATED_TO' link between them with 'shared_infrastructure' reasoning.
        """
        logger.info("running_inference_shared_infrastructure")
        
        # Find all IPs
        ips = self.db.query(GraphEntity).filter_by(entity_type="IP_ADDRESS", status=EntityStatus.ACTIVE).all()
        for ip in ips:
            # Find domains that resolve to this IP
            resolving_rels = self.db.query(GraphRelationship).filter_by(
                target_id=ip.id, 
                relationship_type="RESOLVES_TO"
            ).all()
            
            domain_ids = [rel.source_id for rel in resolving_rels]
            
            # If multiple domains resolve to the same IP, link them
            if len(domain_ids) > 1:
                for i in range(len(domain_ids)):
                    for j in range(i+1, len(domain_ids)):
                        self.rel_manager.create_relationship(
                            source_id=domain_ids[i],
                            target_id=domain_ids[j],
                            rel_type="RELATED_TO",
                            confidence=0.8,
                            properties={"inferred_by": "shared_ip", "ip_id": ip.id}
                        )

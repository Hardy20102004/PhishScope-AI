import structlog
from sqlalchemy.orm import Session

from app.knowledge_graph.managers import EntityManager, RelationshipManager
from app.models.knowledge_graph import EntityStatus, GraphEntity, GraphRelationship

logger = structlog.get_logger("phoenix.kg.inference")

class InferenceEngine:
    """
    Automatically deduces new relationships based on graph proximity and rules.
    """
    def __init__(self, db: Session):
        self.db = db
        self.entity_manager = EntityManager(db)
        self.rel_manager = RelationshipManager(db)

    def run_all_inferences(self):
        self.infer_shared_infrastructure()
        self.infer_shared_malware()
        self.infer_campaign_overlap()

    def infer_shared_infrastructure(self):
        """
        Infers SHARED_INFRASTRUCTURE between Threat Actors if they use the same IP/Domain.
        """
        logger.info("running_inference_shared_infrastructure")
        
        # Example logic: Find IPs
        ips = self.db.query(GraphEntity).filter_by(entity_type="IPV4", status=EntityStatus.ACTIVE).all()
        for ip in ips:
            # Simplistic for prototype: find actors connected to this IP (via domains or directly)
            # In a real scenario, this would be a recursive CTE or NetworkX query.
            pass # Abstracted for brevity

    def infer_shared_malware(self):
        """
        If two Threat Actors USE the same Malware Family, they are RELATED_TO.
        """
        logger.info("running_inference_shared_malware")
        malwares = self.db.query(GraphEntity).filter_by(entity_type="MALWARE_FAMILY", status=EntityStatus.ACTIVE).all()
        for mw in malwares:
            uses_rels = self.db.query(GraphRelationship).filter_by(
                target_id=mw.id, 
                relationship_type="USES"
            ).all()
            
            actor_ids = [rel.source_id for rel in uses_rels]
            
            if len(actor_ids) > 1:
                for i in range(len(actor_ids)):
                    for j in range(i+1, len(actor_ids)):
                        self.rel_manager.create_relationship(
                            source_id=actor_ids[i],
                            target_id=actor_ids[j],
                            rel_type="RELATED_TO",
                            confidence=0.7,
                            is_inferred=True,
                            properties={"inferred_by": "shared_malware", "malware_id": mw.id}
                        )

    def infer_campaign_overlap(self):
        """
        If two Campaigns target the same Organization and Use the same Tool, merge/link them.
        """
        logger.info("running_inference_campaign_overlap")
        pass # Abstracted for brevity

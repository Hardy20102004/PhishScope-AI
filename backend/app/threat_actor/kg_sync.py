from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional

from app.threat_actor.models import ThreatActor, InfrastructureAssociation
from app.knowledge_graph.managers import EntityManager, RelationshipManager
from app.models.knowledge_graph import GraphEntity, GraphRelationship

class ThreatActorKGSync:
    """
    Synchronizes Threat Actor profiles to the Enterprise Knowledge Graph.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.entity_manager = EntityManager(db)
        self.rel_manager = RelationshipManager(db)

    def sync_actor(self, actor: ThreatActor) -> Optional[GraphEntity]:
        """
        Creates or updates a Threat Actor node in the Knowledge Graph.
        """
        try:
            properties = {
                "actor_id": str(actor.id),
                "description": actor.description,
                "status": actor.status,
            }
            if actor.target_sectors:
                properties["sectors"] = actor.target_sectors
                
            tenant_id_str = str(actor.tenant_id) if actor.tenant_id else None

            return self.entity_manager.create_entity(
                entity_type="THREAT_ACTOR",
                name=actor.name,
                tenant_id=tenant_id_str,
                properties=properties,
                confidence=actor.confidence
            )
        except Exception as e:
            logger.error(f"Failed to sync Threat Actor to KG: {e}")
            return None

    def sync_infrastructure(self, actor: ThreatActor, infra: InfrastructureAssociation, ioc_node_id: str) -> Optional[GraphRelationship]:
        """
        Creates an edge between a Threat Actor and an IOC node.
        `ioc_node_id` is the string UUID of the IOC in the Knowledge Graph.
        """
        try:
            actor_node = self.sync_actor(actor)
            if not actor_node:
                return None

            return self.rel_manager.create_relationship(
                source_id=str(actor_node.id),
                target_id=ioc_node_id,
                rel_type="USES",
                weight=1.0,
                confidence=actor.confidence,
                properties={"usage": infra.usage}
            )
        except Exception as e:
            logger.error(f"Failed to sync Infrastructure relationship to KG: {e}")
            return None

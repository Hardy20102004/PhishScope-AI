from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional

from app.models.threat_intel import Indicator, IndicatorCorrelation
from app.knowledge_graph.managers import EntityManager, RelationshipManager
from app.models.knowledge_graph import GraphEntity, GraphRelationship

class KGSyncService:
    """
    Synchronizes IOC Correlation Engine data to the Enterprise Knowledge Graph.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.entity_manager = EntityManager(db)
        self.rel_manager = RelationshipManager(db)

    def _map_ioc_type_to_entity_type(self, ioc_type: str) -> str:
        # Standardize IOC Types to STIX/Ontology entity types
        mapping = {
            "IPv4": "IP_ADDRESS",
            "IPv6": "IP_ADDRESS",
            "Domain": "DOMAIN",
            "Subdomain": "SUBDOMAIN",
            "URL": "URL",
            "Email Address": "EMAIL_ADDRESS",
            "SHA256": "HASH",
            "SHA1": "HASH",
            "MD5": "HASH",
            "File Name": "FILE",
            "TLS Certificate": "TLS_CERTIFICATE",
        }
        return mapping.get(ioc_type, "IOC")

    def sync_indicator(self, indicator: Indicator) -> Optional[GraphEntity]:
        """
        Creates or updates a node in the Knowledge Graph for an Indicator.
        """
        try:
            entity_type = self._map_ioc_type_to_entity_type(indicator.type)
            
            properties = {
                "indicator_id": str(indicator.id),
                "type": indicator.type,
                "normalized_value": indicator.normalized_value,
                "source_module": indicator.source_module,
                "reputation_score": indicator.reputation_score
            }

            if indicator.raw_context:
                properties["raw_context"] = indicator.raw_context
                
            tenant_id_str = str(indicator.tenant_id) if indicator.tenant_id else None

            # Assuming normalized_value is the unique "name" for deduplication in KG
            return self.entity_manager.create_entity(
                entity_type=entity_type,
                name=indicator.normalized_value,
                tenant_id=tenant_id_str,
                properties=properties,
                confidence=1.0 # High confidence it exists since we saw it
            )
        except Exception as e:
            logger.error(f"Failed to sync indicator to KG: {e}")
            return None

    def sync_relationship(self, relationship: IndicatorCorrelation, source_indicator: Indicator, target_indicator: Indicator) -> Optional[GraphRelationship]:
        """
        Creates an edge in the Knowledge Graph for an IOC Relationship.
        Assumes both entities already exist in the graph.
        """
        try:
            # First ensure both are in the KG
            source_node = self.sync_indicator(source_indicator)
            target_node = self.sync_indicator(target_indicator)
            
            if not source_node or not target_node:
                return None

            properties = {
                "relationship_id": str(relationship.id),
                "similarity_score": relationship.similarity_score
            }

            return self.rel_manager.create_relationship(
                source_id=str(source_node.id),
                target_id=str(target_node.id),
                rel_type=relationship.correlation_type.replace(" ", "_").upper(), # E.g. "SHARED_INFRASTRUCTURE"
                weight=1.0,
                confidence=relationship.confidence,
                properties=properties
            )
            
        except Exception as e:
            logger.error(f"Failed to sync relationship to KG: {e}")
            return None

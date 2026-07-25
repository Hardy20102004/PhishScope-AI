from typing import Any, Dict, Optional

import structlog
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.knowledge_graph.ontology import OntologyManager
from app.models.knowledge_graph import (
    EntityStatus,
    GraphEntity,
    GraphRelationship,
    RelationshipStatus,
)

logger = structlog.get_logger("phoenix.kg.managers")

class EntityManager:
    def __init__(self, db: Session):
        self.db = db
        self.ontology = OntologyManager()

    def create_entity(self, entity_type: str, name: str, tenant_id: Optional[str] = None, properties: Dict[str, Any] = None, confidence: float = 1.0) -> GraphEntity:
        if not self.ontology.validate_entity_type(entity_type):
            logger.warning("invalid_entity_type_created", type=entity_type)
            # In strict mode we might raise an error here.
            
        # Deduplication check (find active entity with same type/name/tenant)
        existing = self.db.query(GraphEntity).filter_by(
            entity_type=entity_type.upper(),
            name=name,
            tenant_id=tenant_id,
            status=EntityStatus.ACTIVE
        ).first()
        
        if existing:
            # Merge properties and return existing
            if properties:
                existing.properties_json.update(properties)
                self.db.commit()
                self.db.refresh(existing)
            return existing

        entity = GraphEntity(
            entity_type=entity_type.upper(),
            name=name,
            tenant_id=tenant_id,
            confidence=confidence,
            properties_json=properties or {}
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_entity(self, entity_id: str) -> Optional[GraphEntity]:
        return self.db.query(GraphEntity).filter_by(id=entity_id).first()


class RelationshipManager:
    def __init__(self, db: Session):
        self.db = db
        self.ontology = OntologyManager()
        self.entity_manager = EntityManager(db)

    def create_relationship(self, source_id: str, target_id: str, rel_type: str, weight: float = 1.0, confidence: float = 1.0, properties: Dict[str, Any] = None) -> GraphRelationship:
        source = self.entity_manager.get_entity(source_id)
        target = self.entity_manager.get_entity(target_id)
        
        if not source or not target:
            raise ValueError("Source or target entity does not exist.")

        if not self.ontology.validate_relationship_type(rel_type):
            logger.warning("invalid_rel_type_created", type=rel_type)

        self.ontology.is_valid_triple(source.entity_type, rel_type, target.entity_type)

        # Check for existing relationship
        existing = self.db.query(GraphRelationship).filter_by(
            source_id=source_id,
            target_id=target_id,
            relationship_type=rel_type.upper()
        ).first()

        if existing:
            # Update weight/confidence/properties
            existing.weight = max(existing.weight, weight)
            existing.confidence = max(existing.confidence, confidence)
            if properties:
                existing.properties_json.update(properties)
            existing.status = RelationshipStatus.ACTIVE
            self.db.commit()
            self.db.refresh(existing)
            return existing

        rel = GraphRelationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=rel_type.upper(),
            weight=weight,
            confidence=confidence,
            properties_json=properties or {}
        )
        self.db.add(rel)
        try:
            self.db.commit()
            self.db.refresh(rel)
        except IntegrityError:
            self.db.rollback()
            # If concurrent creation happened
            return self.db.query(GraphRelationship).filter_by(
                source_id=source_id, target_id=target_id, relationship_type=rel_type.upper()
            ).first()
            
        return rel

from typing import Any, Dict, Optional
from datetime import datetime

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

    def create_entity(
        self, 
        entity_type: str, 
        name: str, 
        tenant_id: Optional[str] = None, 
        properties: Dict[str, Any] = None, 
        confidence: float = 1.0,
        observed_start: Optional[datetime] = None,
        observed_end: Optional[datetime] = None
    ) -> GraphEntity:
        
        if not self.ontology.validate_entity_type(entity_type):
            logger.warning("invalid_entity_type_created", type=entity_type)
            
        existing = self.db.query(GraphEntity).filter_by(
            entity_type=entity_type.upper(),
            name=name,
            tenant_id=tenant_id,
            status=EntityStatus.ACTIVE
        ).first()
        
        if existing:
            if properties:
                existing.properties_json.update(properties)
            if observed_start and (not existing.observed_start or observed_start < existing.observed_start):
                existing.observed_start = observed_start
            if observed_end and (not existing.observed_end or observed_end > existing.observed_end):
                existing.observed_end = observed_end
                
            self.db.commit()
            self.db.refresh(existing)
            return existing

        entity = GraphEntity(
            entity_type=entity_type.upper(),
            name=name,
            tenant_id=tenant_id,
            confidence=confidence,
            observed_start=observed_start,
            observed_end=observed_end,
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

    def create_relationship(
        self, 
        source_id: str, 
        target_id: str, 
        rel_type: str, 
        weight: float = 1.0, 
        confidence: float = 1.0, 
        is_inferred: bool = False,
        observed_start: Optional[datetime] = None,
        observed_end: Optional[datetime] = None,
        properties: Dict[str, Any] = None
    ) -> GraphRelationship:
        
        source = self.entity_manager.get_entity(source_id)
        target = self.entity_manager.get_entity(target_id)
        
        if not source or not target:
            raise ValueError("Source or target entity does not exist.")

        if not self.ontology.validate_relationship_type(rel_type):
            logger.warning("invalid_rel_type_created", type=rel_type)

        self.ontology.is_valid_triple(source.entity_type, rel_type, target.entity_type)

        existing = self.db.query(GraphRelationship).filter_by(
            source_id=source_id,
            target_id=target_id,
            relationship_type=rel_type.upper()
        ).first()

        if existing:
            existing.weight = max(existing.weight, weight)
            existing.confidence = max(existing.confidence, confidence)
            if not existing.is_inferred and is_inferred:
                pass # Confirmed edge overrides inferred
            else:
                existing.is_inferred = is_inferred
                
            if observed_start and (not existing.observed_start or observed_start < existing.observed_start):
                existing.observed_start = observed_start
            if observed_end and (not existing.observed_end or observed_end > existing.observed_end):
                existing.observed_end = observed_end
                
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
            is_inferred=is_inferred,
            observed_start=observed_start,
            observed_end=observed_end,
            properties_json=properties or {}
        )
        self.db.add(rel)
        try:
            self.db.commit()
            self.db.refresh(rel)
        except IntegrityError:
            self.db.rollback()
            return self.db.query(GraphRelationship).filter_by(
                source_id=source_id, target_id=target_id, relationship_type=rel_type.upper()
            ).first()
            
        return rel

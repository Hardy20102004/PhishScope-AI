from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from app.db.base_class import Base

class EntityStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    MERGED = "MERGED"
    DELETED = "DELETED"

class RelationshipStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    DELETED = "DELETED"

class GraphEntity(Base):
    __tablename__ = "kg_entities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type = Column(String, nullable=False, index=True) # e.g. IP_ADDRESS, THREAT_ACTOR, CAMPAIGN
    name = Column(String, nullable=False, index=True)
    tenant_id = Column(String, nullable=True, index=True)
    status = Column(Enum(EntityStatus), default=EntityStatus.ACTIVE)
    
    confidence = Column(Float, default=1.0)
    
    properties_json = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Note: For adjacency list, we map outgoing and incoming edges
    outgoing_relationships = relationship("GraphRelationship", foreign_keys="[GraphRelationship.source_id]", back_populates="source_entity", cascade="all, delete-orphan")
    incoming_relationships = relationship("GraphRelationship", foreign_keys="[GraphRelationship.target_id]", back_populates="target_entity", cascade="all, delete-orphan")


class GraphRelationship(Base):
    __tablename__ = "kg_relationships"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False, index=True)
    target_id = Column(String, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False, index=True)
    
    relationship_type = Column(String, nullable=False, index=True) # e.g. BELONGS_TO, TARGETS, COMMUNICATES_WITH
    status = Column(Enum(RelationshipStatus), default=RelationshipStatus.ACTIVE)
    
    weight = Column(Float, default=1.0)
    confidence = Column(Float, default=1.0)
    
    properties_json = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    source_entity = relationship("GraphEntity", foreign_keys=[source_id], back_populates="outgoing_relationships")
    target_entity = relationship("GraphEntity", foreign_keys=[target_id], back_populates="incoming_relationships")
    
    __table_args__ = (
        UniqueConstraint('source_id', 'target_id', 'relationship_type', name='uq_graph_edge'),
    )

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Uuid, Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class OntologyType(str, enum.Enum):
    ENTITY_TYPE = "ENTITY_TYPE"
    RELATIONSHIP_TYPE = "RELATIONSHIP_TYPE"
    TAXONOMY = "TAXONOMY"
    SEMANTIC_MODEL = "SEMANTIC_MODEL"

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class OntologyNode(Base):
    __tablename__ = "knowledge_ontology_nodes"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    type = Column(SQLEnum(OntologyType), nullable=False)
    description = Column(String, nullable=True)
    
    properties = Column(JSON, default=dict)
    schema_version = Column(String, default="1.0")
    
    status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    approved_by = Column(Uuid(as_uuid=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class SchemaRecommendation(Base):
    __tablename__ = "knowledge_schema_recommendations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    target_node_id = Column(Uuid(as_uuid=True), ForeignKey("knowledge_ontology_nodes.id"), nullable=True)
    
    recommendation_type = Column(String, nullable=False) # e.g. "ADD_PROPERTY", "MERGE_ENTITIES"
    description = Column(String, nullable=False)
    evidence = Column(JSON, default=dict)
    
    status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EvolutionQualityMetric(Base):
    __tablename__ = "knowledge_evolution_quality_metrics"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    coverage_score = Column(Integer, nullable=False) # 0-100
    consistency_score = Column(Integer, nullable=False) # 0-100
    freshness_score = Column(Integer, nullable=False) # 0-100
    confidence_score = Column(Integer, nullable=False) # 0-100
    relationship_quality = Column(Integer, nullable=False) # 0-100
    
    details = Column(JSON, default=dict)
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

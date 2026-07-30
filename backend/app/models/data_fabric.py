import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class MetadataType(str, enum.Enum):
    DATA_SOURCE = "DATA_SOURCE"
    SCHEMA = "SCHEMA"
    BUSINESS_GLOSSARY = "BUSINESS_GLOSSARY"
    ASSET = "ASSET"
    IDENTITY = "IDENTITY"
    RISK = "RISK"
    GOVERNANCE_POLICY = "GOVERNANCE_POLICY"

class QualityStatus(str, enum.Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    CRITICAL = "CRITICAL"

class MetadataNode(Base):
    __tablename__ = "data_fabric_metadata_nodes"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(SQLEnum(MetadataType), nullable=False)
    description = Column(String, nullable=True)
    
    properties = Column(JSON, default=dict)
    tags = Column(JSON, default=list)
    
    owner_id = Column(Uuid(as_uuid=True), nullable=True)
    classification_label = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class LineageEdge(Base):
    __tablename__ = "data_fabric_lineage_edges"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    source_node_id = Column(Uuid(as_uuid=True), ForeignKey("data_fabric_metadata_nodes.id"), nullable=False)
    target_node_id = Column(Uuid(as_uuid=True), ForeignKey("data_fabric_metadata_nodes.id"), nullable=False)
    
    transformation_type = Column(String, nullable=False)
    pipeline_name = Column(String, nullable=True)
    details = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source_node = relationship("MetadataNode", foreign_keys=[source_node_id])
    target_node = relationship("MetadataNode", foreign_keys=[target_node_id])

class QualityMetric(Base):
    __tablename__ = "data_fabric_quality_metrics"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    node_id = Column(Uuid(as_uuid=True), ForeignKey("data_fabric_metadata_nodes.id"), nullable=False)
    
    completeness_score = Column(Integer, nullable=False) # 0-100
    consistency_score = Column(Integer, nullable=False) # 0-100
    freshness_score = Column(Integer, nullable=False) # 0-100
    accuracy_score = Column(Integer, nullable=False) # 0-100
    
    overall_status = Column(SQLEnum(QualityStatus), nullable=False)
    confidence = Column(Integer, nullable=False) # 0-100
    
    details = Column(JSON, default=dict)
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    node = relationship("MetadataNode")

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Float, Text, Boolean, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class MemoryType(str, enum.Enum):
    WORKING = "WORKING"
    SESSION = "SESSION"
    CONVERSATION = "CONVERSATION"
    CASE = "CASE"
    INVESTIGATION = "INVESTIGATION"
    EVIDENCE = "EVIDENCE"
    THREAT_INTEL = "THREAT_INTEL"
    ORGANIZATION = "ORGANIZATION"
    TENANT = "TENANT"
    USER_PREFERENCE = "USER_PREFERENCE"
    POLICY = "POLICY"
    WORKFLOW = "WORKFLOW"
    AI_LEARNING = "AI_LEARNING"
    KNOWLEDGE = "KNOWLEDGE"
    HISTORICAL = "HISTORICAL"
    ARCHIVE = "ARCHIVE"

class RelationType(str, enum.Enum):
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_MANY = "MANY_TO_MANY"
    PARENT_CHILD = "PARENT_CHILD"
    TEMPORAL = "TEMPORAL"
    EVIDENCE = "EVIDENCE"
    THREAT = "THREAT"

class SecurityClassification(str, enum.Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"

class MemoryItem(Base):
    """
    Core relational schema for persistent memories in the AI Memory Engine.
    Vector data is referenced via vector_id to the Vector Database.
    """
    __tablename__ = "ai_memories"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    memory_type = Column(String, nullable=False, default=MemoryType.WORKING.value) # Use String instead of Enum for SQLite compat
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Ownership and Isolation
    owner_id = Column(String(36), nullable=True) # Could be user_id or agent_id
    tenant_id = Column(String(36), nullable=False, default="default-tenant")
    organization_id = Column(String(36), nullable=True)
    
    # Graph / Entity Links
    case_id = Column(String(36), nullable=True)
    investigation_id = Column(String(36), nullable=True)
    
    # Engine Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    
    version = Column(Integer, default=1, nullable=False)
    security_classification = Column(String, default=SecurityClassification.INTERNAL.value, nullable=False)
    retention_policy = Column(String, default="default", nullable=False)
    confidence_score = Column(Float, default=1.0)
    source = Column(String, nullable=True)
    
    # Vector store reference (Hybrid DB linkage)
    vector_id = Column(String(36), nullable=True)
    
    # Relationships
    relationships_source = relationship("MemoryRelationship", foreign_keys="MemoryRelationship.source_id", back_populates="source_memory")
    relationships_target = relationship("MemoryRelationship", foreign_keys="MemoryRelationship.target_id", back_populates="target_memory")

class MemoryRelationship(Base):
    """
    Edges for the Knowledge Graph integration.
    """
    __tablename__ = "ai_memory_relationships"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("ai_memories.id"), nullable=False)
    target_id = Column(String(36), ForeignKey("ai_memories.id"), nullable=False)
    relation_type = Column(String, nullable=False)
    weight = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    source_memory = relationship("MemoryItem", foreign_keys=[source_id], back_populates="relationships_source")
    target_memory = relationship("MemoryItem", foreign_keys=[target_id], back_populates="relationships_target")

class MemoryAuditLog(Base):
    """
    Audit logging for memory operations (Creation, Read, Update, Delete) to ensure security and compliance.
    """
    __tablename__ = "ai_memory_audit_logs"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    memory_id = Column(String(36), nullable=False)
    action_type = Column(String, nullable=False) # e.g., READ, UPDATE, DELETE, EXPIRE
    actor_id = Column(String(36), nullable=False) # User or Agent
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    details = Column(Text, nullable=True)

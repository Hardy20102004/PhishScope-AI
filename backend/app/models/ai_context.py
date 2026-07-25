import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Integer, Float, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class ContextPolicyType(str, enum.Enum):
    REDACT_PII = "REDACT_PII"
    TENANT_ISOLATION = "TENANT_ISOLATION"
    MAX_TOKENS = "MAX_TOKENS"
    MANDATORY_EVIDENCE = "MANDATORY_EVIDENCE"
    RESTRICT_CLASSIFICATION = "RESTRICT_CLASSIFICATION"

class ContextTemplate(Base):
    """
    Predefined context structures (e.g., Threat Analysis vs Incident Report).
    """
    __tablename__ = "ai_context_templates"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    base_prompt = Column(Text, nullable=False)
    default_max_tokens = Column(Integer, default=4096)
    created_at = Column(DateTime, default=datetime.utcnow)

class ContextCacheEntry(Base):
    """
    Stores pre-built context segments to save retrieval time.
    """
    __tablename__ = "ai_context_cache"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    cache_key = Column(String(255), nullable=False, unique=True, index=True)
    assembled_context = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

class ContextAuditLog(Base):
    """
    Tracks context generation, validation failures, and optimization metrics.
    """
    __tablename__ = "ai_context_audit_logs"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String(36), nullable=True)
    actor_id = Column(String(36), nullable=False)
    action = Column(String, nullable=False) # e.g. "BUILD", "VALIDATION_FAILED"
    details = Column(Text, nullable=True)
    
    # Optimization Metrics
    original_tokens = Column(Integer, nullable=True)
    compressed_tokens = Column(Integer, nullable=True)
    build_latency_ms = Column(Float, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)

class ContextPolicy(Base):
    """
    Rules enforced by the Policy Engine on context assembly.
    """
    __tablename__ = "ai_context_policies"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    policy_type = Column(String, nullable=False) # ContextPolicyType
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    configuration = Column(Text, nullable=True) # JSON config
    tenant_id = Column(String(36), nullable=True) # If null, applies globally

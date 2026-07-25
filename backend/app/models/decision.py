import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DecisionState(str, enum.Enum):
    DRAFT = "DRAFT"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVISED = "REVISED"

class DecisionType(str, enum.Enum):
    THREAT_CLASSIFICATION = "THREAT_CLASSIFICATION"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    EVIDENCE_PRIORITIZATION = "EVIDENCE_PRIORITIZATION"
    INVESTIGATION_PRIORITIZATION = "INVESTIGATION_PRIORITIZATION"
    CASE_ESCALATION = "CASE_ESCALATION"
    NEXT_STEPS = "NEXT_STEPS"
    MITIGATION = "MITIGATION"
    EVIDENCE_GAP = "EVIDENCE_GAP"
    THREAT_HUNT = "THREAT_HUNT"
    CASE_CLOSURE = "CASE_CLOSURE"

class DecisionRecord(Base):
    __tablename__ = "decisions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=True, index=True)
    case_id = Column(String, nullable=True, index=True)
    
    decision_type = Column(Enum(DecisionType), nullable=False, index=True)
    state = Column(Enum(DecisionState), default=DecisionState.DRAFT, index=True)
    
    # High-level summary of what the engine decided
    summary = Column(Text, nullable=False)
    
    # Confidence score 0.0 -> 1.0
    confidence = Column(Float, nullable=False)
    
    # JSON arrays for complex objects
    reasoning_chain = Column(JSON, default=list) # List of reasoning steps
    assumptions = Column(JSON, default=list)
    limitations = Column(JSON, default=list)
    alternatives = Column(JSON, default=list) # Hypotheses
    recommendations = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    evidence_links = relationship("DecisionEvidenceLink", back_populates="decision", cascade="all, delete-orphan")
    workflow_logs = relationship("ApprovalWorkflow", back_populates="decision", cascade="all, delete-orphan")

class DecisionEvidenceLink(Base):
    __tablename__ = "decision_evidence_links"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    decision_id = Column(String, ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # The source of the evidence (e.g. KNOWLEDGE_GRAPH, RAG_DOCUMENT, RAW_LOG)
    source_type = Column(String, nullable=False)
    # The ID within that source (e.g. GraphEntity ID or DocumentChunk ID)
    source_id = Column(String, nullable=False, index=True)
    
    description = Column(String, nullable=True) # How it supports the decision
    
    decision = relationship("DecisionRecord", back_populates="evidence_links")


class ApprovalWorkflow(Base):
    """Audit log for human interaction with a decision"""
    __tablename__ = "decision_approval_workflows"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    decision_id = Column(String, ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, nullable=False)
    
    action = Column(String, nullable=False) # e.g. APPROVED, REJECTED, OVERRIDDEN
    comments = Column(Text, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    decision = relationship("DecisionRecord", back_populates="workflow_logs")

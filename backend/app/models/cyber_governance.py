import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Uuid, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class GovernanceStatus(str, enum.Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    AT_RISK = "AT_RISK"
    NOT_EVALUATED = "NOT_EVALUATED"

class PolicyStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    IN_REVIEW = "IN_REVIEW"

class CyberGovernanceKPI(Base):
    __tablename__ = "governance_kpi"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    metric_name = Column(String, index=True, nullable=False)
    metric_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)
    
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class GovernancePolicy(Base):
    __tablename__ = "governance_policy"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    version = Column(String, default="1.0")
    framework = Column(String, index=True, nullable=False) # e.g., ISO 27001, NIST CSF
    
    status = Column(SQLEnum(PolicyStatus), default=PolicyStatus.DRAFT)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    next_review_date = Column(DateTime(timezone=True), nullable=True)

class RiskOversightMetric(Base):
    __tablename__ = "governance_risk_oversight"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    risk_domain = Column(String, index=True, nullable=False) # Enterprise, Cloud, Identity
    risk_score = Column(Float, nullable=False)
    confidence_level = Column(Float, nullable=False) # AI calculated confidence
    
    details = Column(JSON, default=dict)
    
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class BoardReportSummary(Base):
    __tablename__ = "governance_board_report"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    quarter = Column(String, nullable=False) # e.g., Q3 2026
    
    summary_text = Column(String, nullable=False)
    investment_summary = Column(JSON, default=dict)
    risk_summary = Column(JSON, default=dict)
    
    generated_by_ai = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

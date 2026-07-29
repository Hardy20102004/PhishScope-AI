import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class DetectionRule(Base):
    __tablename__ = "detection_rules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rule_type: Mapped[str] = mapped_column(String(50)) # SIGMA, YARA, CUSTOM
    
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", index=True) # DRAFT, IN_REVIEW, APPROVED, READY_FOR_DEPLOYMENT, DEPLOYED, RETIRED
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    
    mitre_tactics: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    mitre_techniques: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    current_version: Mapped[int] = mapped_column(Integer, default=1)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    versions = relationship("DetectionRuleVersion", back_populates="rule", cascade="all, delete-orphan")
    test_results = relationship("RuleTestResult", back_populates="rule", cascade="all, delete-orphan")
    approvals = relationship("RuleApprovalRecord", back_populates="rule", cascade="all, delete-orphan")


class DetectionRuleVersion(Base):
    __tablename__ = "detection_rule_versions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    rule_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("detection_rules.id", ondelete="CASCADE"), index=True)
    
    version: Mapped[int] = mapped_column(Integer)
    payload: Mapped[str] = mapped_column(Text) # Raw YAML, JSON, or YARA text
    change_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    rule = relationship("DetectionRule", back_populates="versions")


class RuleTestResult(Base):
    __tablename__ = "detection_rule_test_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    rule_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("detection_rules.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("detection_rule_versions.id", ondelete="CASCADE"))
    
    dataset_name: Mapped[str] = mapped_column(String(255))
    coverage_score: Mapped[float] = mapped_column(Float, default=0.0)
    false_positives: Mapped[int] = mapped_column(Integer, default=0)
    false_negatives: Mapped[int] = mapped_column(Integer, default=0)
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    rule = relationship("DetectionRule", back_populates="test_results")


class RuleApprovalRecord(Base):
    __tablename__ = "detection_rule_approvals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    rule_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("detection_rules.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("detection_rule_versions.id", ondelete="CASCADE"))
    
    approver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status_changed_to: Mapped[str] = mapped_column(String(50))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    rule = relationship("DetectionRule", back_populates="approvals")

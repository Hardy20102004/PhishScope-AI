import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class Alert(Base):
    __tablename__ = "security_alerts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    # Core Data
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(100), index=True) # EDR, SIEM, FIREWALL
    source_alert_id: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    severity: Mapped[str] = mapped_column(String(50)) # LOW, MEDIUM, HIGH, CRITICAL
    
    # Enrichment & AI
    priority_score: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    mitre_techniques: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # State & Lifecycle
    status: Mapped[str] = mapped_column(String(50), default="NEW", index=True) # NEW, ASSIGNED, IN_INVESTIGATION, RESOLVED, CLOSED
    resolution_reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Graph / Correlation
    correlation_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("alert_correlation_groups.id", ondelete="SET NULL"), nullable=True, index=True)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("cases.id", ondelete="SET NULL"), nullable=True, index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    evidence = relationship("AlertEvidence", back_populates="alert", cascade="all, delete-orphan")
    assignments = relationship("AlertAssignment", back_populates="alert", cascade="all, delete-orphan")
    lifecycle_events = relationship("AlertLifecycleEvent", back_populates="alert", cascade="all, delete-orphan")
    correlation_group = relationship("AlertCorrelationGroup", back_populates="alerts")


class AlertEvidence(Base):
    __tablename__ = "alert_evidence"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    alert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("security_alerts.id", ondelete="CASCADE"), index=True)
    
    evidence_type: Mapped[str] = mapped_column(String(100)) # IP, DOMAIN, HASH, USER, HOST
    value: Mapped[str] = mapped_column(String(255), index=True)
    context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    alert = relationship("Alert", back_populates="evidence")


class AlertCorrelationGroup(Base):
    __tablename__ = "alert_correlation_groups"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    correlation_reason: Mapped[str] = mapped_column(String(255)) # SHARED_IOC, THREAT_ACTOR, CAMPAIGN
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    alerts = relationship("Alert", back_populates="correlation_group")


class AlertAssignment(Base):
    __tablename__ = "alert_assignments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    alert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("security_alerts.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    alert = relationship("Alert", back_populates="assignments")
    # user = relationship("User")


class AlertLifecycleEvent(Base):
    __tablename__ = "alert_lifecycle_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    alert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("security_alerts.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    previous_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    new_status: Mapped[str] = mapped_column(String(50))
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    alert = relationship("Alert", back_populates="lifecycle_events")

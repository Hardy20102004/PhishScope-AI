"""
PHOENIX X — Phase X-092
Enterprise AI Security Orchestration, Decision Intelligence & Human-Governed Security Automation Platform
Database Models
"""
import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey, Integer,
    String, Text, JSON, Enum
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

# ─────────────────────────────────────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────────────────────────────────────

class WorkflowType(str, enum.Enum):
    INCIDENT_RESPONSE = "INCIDENT_RESPONSE"
    THREAT_HUNTING = "THREAT_HUNTING"
    IDENTITY_REVIEW = "IDENTITY_REVIEW"
    CLOUD_GOVERNANCE = "CLOUD_GOVERNANCE"
    APPROVAL_GATE = "APPROVAL_GATE"

class WorkflowStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class TaskStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class AuthorizationStatus(str, enum.Enum):
    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"

# ─────────────────────────────────────────────────────────────────────────────
# Workflows & Playbooks
# ─────────────────────────────────────────────────────────────────────────────

class WorkflowRecord(Base):
    """
    Tracks end-to-end incident, threat hunting, or governance workflows.
    """
    __tablename__ = "orchestration_workflows"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workflow_type: Mapped[WorkflowType] = mapped_column(Enum(WorkflowType), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[WorkflowStatus] = mapped_column(Enum(WorkflowStatus), default=WorkflowStatus.QUEUED)
    
    context_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class PlaybookDefinition(Base):
    """
    Defines standard operating procedures and human-approval gates.
    """
    __tablename__ = "orchestration_playbooks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")
    
    requires_human_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    steps: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ─────────────────────────────────────────────────────────────────────────────
# Tasks & Decisions
# ─────────────────────────────────────────────────────────────────────────────

class TaskAssignment(Base):
    """
    Individual tasks assigned to analysts or AI agents within a workflow.
    """
    __tablename__ = "orchestration_tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workflow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orchestration_workflows.id", ondelete="CASCADE"))
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # User ID or "AI_AGENT"
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.OPEN)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class OrchestrationDecisionLog(Base):
    """
    AI-generated recommendations and the human authorizations recorded against them.
    """
    __tablename__ = "orchestration_decision_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workflow_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("orchestration_workflows.id", ondelete="CASCADE"), nullable=True)
    
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=True)
    
    authorization_status: Mapped[AuthorizationStatus] = mapped_column(Enum(AuthorizationStatus), default=AuthorizationStatus.PENDING)
    authorized_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

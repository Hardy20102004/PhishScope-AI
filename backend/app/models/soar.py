import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class Playbook(Base):
    __tablename__ = "soar_playbooks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT") # DRAFT, PUBLISHED, ARCHIVED
    version: Mapped[int] = mapped_column(Integer, default=1)
    
    workflow_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict) # Stores nodes, edges, config
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    executions = relationship("ExecutionHistory", back_populates="playbook", cascade="all, delete-orphan")


class ExecutionHistory(Base):
    __tablename__ = "soar_execution_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    playbook_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("soar_playbooks.id", ondelete="CASCADE"), index=True)
    incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ir_incidents.id", ondelete="SET NULL"), nullable=True, index=True)
    
    status: Mapped[str] = mapped_column(String(50), default="RUNNING") # RUNNING, PAUSED_FOR_APPROVAL, COMPLETED, FAILED, CANCELLED
    current_step_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    execution_log: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list) # Detailed log of executed steps
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    playbook = relationship("Playbook", back_populates="executions")
    approvals = relationship("ApprovalRecord", back_populates="execution", cascade="all, delete-orphan")


class ApprovalRecord(Base):
    __tablename__ = "soar_approval_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    execution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("soar_execution_history.id", ondelete="CASCADE"), index=True)
    
    step_id: Mapped[str] = mapped_column(String(255))
    action_requested: Mapped[str] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED
    reviewed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    review_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    execution = relationship("ExecutionHistory", back_populates="approvals")

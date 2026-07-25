import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, JSON, Uuid, Text, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
import enum

class TriggerType(str, enum.Enum):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"
    CASE_CREATED = "CASE_CREATED"
    EVIDENCE_ADDED = "EVIDENCE_ADDED"
    WEBHOOK = "WEBHOOK"

class ExecutionStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    trigger_type: Mapped[TriggerType] = mapped_column(SQLEnum(TriggerType), default=TriggerType.MANUAL, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    versions = relationship("WorkflowVersion", back_populates="workflow", cascade="all, delete-orphan", order_by="WorkflowVersion.version_number.desc()")

class WorkflowVersion(Base):
    __tablename__ = "workflow_versions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workflow_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), index=True, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    # JSON graph containing nodes and edges for ReactFlow
    definition_json: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    workflow = relationship("Workflow", back_populates="versions")
    executions = relationship("WorkflowExecution", back_populates="version", cascade="all, delete-orphan")

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    version_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("workflow_versions.id", ondelete="CASCADE"), index=True, nullable=False)
    
    trigger_event_json: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[ExecutionStatus] = mapped_column(SQLEnum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False)
    logs_json: Mapped[list] = mapped_column(JSON, default=list) # [{node_id: "xyz", status: "success", output: "..."}]
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    version = relationship("WorkflowVersion", back_populates="executions")

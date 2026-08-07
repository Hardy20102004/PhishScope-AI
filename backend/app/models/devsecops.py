import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class PipelineStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELED = "CANCELED"

class GateStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    ERROR = "ERROR"

class SDLCPhase(str, enum.Enum):
    PLAN = "PLAN"
    CODE = "CODE"
    BUILD = "BUILD"
    TEST = "TEST"
    RELEASE = "RELEASE"
    DEPLOY = "DEPLOY"
    OPERATE = "OPERATE"

class PipelineRun(Base):
    """
    Represents a CI/CD pipeline execution.
    """
    __tablename__ = "devsecops_pipeline_runs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    repository_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_repositories.id", ondelete="SET NULL"), nullable=True)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_applications.id", ondelete="SET NULL"), nullable=True)
    
    ci_provider: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. GITHUB_ACTIONS, GITLAB_CI, JENKINS
    run_identifier: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. GitHub Run ID
    branch: Mapped[str] = mapped_column(String(255), nullable=False)
    commit_sha: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[PipelineStatus] = mapped_column(Enum(PipelineStatus), default=PipelineStatus.QUEUED)
    sdlc_phase: Mapped[SDLCPhase] = mapped_column(Enum(SDLCPhase), default=SDLCPhase.BUILD)
    
    triggered_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Developer email or username
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class SecurityGate(Base):
    """
    Tracks security guardrails within a pipeline run.
    """
    __tablename__ = "devsecops_security_gates"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("devsecops_pipeline_runs.id", ondelete="CASCADE"), index=True)
    
    gate_name: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. "SAST Scan", "SCA Check"
    gate_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    status: Mapped[GateStatus] = mapped_column(Enum(GateStatus), default=GateStatus.PASS)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SDLCWorkflow(Base):
    """
    Orchestrated security workflows, approvals, or exceptions.
    """
    __tablename__ = "devsecops_workflows"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    pipeline_run_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("devsecops_pipeline_runs.id", ondelete="SET NULL"), nullable=True)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_applications.id", ondelete="SET NULL"), nullable=True)
    
    workflow_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "EXCEPTION_REQUEST", "RELEASE_APPROVAL"
    status: Mapped[str] = mapped_column(String(100), default="PENDING")
    
    requester: Mapped[str] = mapped_column(String(255), nullable=False)
    approver: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    justification: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class DeveloperMetric(Base):
    """
    Developer productivity and security metrics.
    """
    __tablename__ = "devsecops_developer_metrics"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    developer_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    code_quality_score: Mapped[float] = mapped_column(Float, default=100.0)
    security_score: Mapped[float] = mapped_column(Float, default=100.0)
    
    vulnerabilities_introduced: Mapped[int] = mapped_column(Integer, default=0)
    vulnerabilities_fixed: Mapped[int] = mapped_column(Integer, default=0)
    
    training_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    last_calculated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DevSecOpsAuditLog(Base):
    """
    Audit log for changes in the DevSecOps platform.
    """
    __tablename__ = "devsecops_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

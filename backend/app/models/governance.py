import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class SecurityPolicy(Base):
    __tablename__ = "mf_gov_policies"
    """
    Represents a defined cloud governance rule.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    policy_name: Mapped[str] = mapped_column(String(255))
    policy_domain: Mapped[str] = mapped_column(String(100)) # IDENTITY, NETWORK, STORAGE
    description: Mapped[str] = mapped_column(Text)
    
    rule_logic: Mapped[dict] = mapped_column(JSON)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class GovernanceWorkflow(Base):
    __tablename__ = "mf_gov_workflows"
    """
    An instance of an orchestrated workflow (e.g., Automated Remediation).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workflow_name: Mapped[str] = mapped_column(String(255))
    workflow_type: Mapped[str] = mapped_column(String(100)) # REMEDIATION, EXCEPTION_REQUEST
    
    status: Mapped[str] = mapped_column(String(50), default="PLANNING") # PLANNING, PENDING_APPROVAL, EXECUTING, COMPLETED, REJECTED
    context_data: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class GovernanceApprovalRecord(Base):
    __tablename__ = "mf_gov_approvals"
    """
    Tracks human approvals tied to a specific workflow step.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workflow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_gov_workflows.id", ondelete="CASCADE"), index=True)
    approver_id: Mapped[str] = mapped_column(String(255)) # ID of the user
    approver_role: Mapped[str] = mapped_column(String(100)) # L1_SOC, L2_SOC, CISO
    
    action: Mapped[str] = mapped_column(String(50)) # APPROVED, REJECTED
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AutomationLog(Base):
    __tablename__ = "mf_gov_automation_logs"
    """
    Immutable record of all automation tasks coordinated by the platform.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workflow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_gov_workflows.id", ondelete="CASCADE"), index=True)
    
    task_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50)) # SUCCESS, FAILED
    execution_details: Mapped[dict] = mapped_column(JSON, default=dict)
    
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

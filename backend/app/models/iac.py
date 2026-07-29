import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class IaCTechnology(str, enum.Enum):
    TERRAFORM = "TERRAFORM"
    CLOUDFORMATION = "CLOUDFORMATION"
    KUBERNETES = "KUBERNETES"
    HELM = "HELM"
    PULUMI = "PULUMI"
    ARM = "ARM"
    BICEP = "BICEP"
    ANSIBLE = "ANSIBLE"
    UNKNOWN = "UNKNOWN"

class IaCDeploymentStatus(str, enum.Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEPLOYED = "DEPLOYED"
    FAILED = "FAILED"

class IaCTemplate(Base):
    """
    Inventory representation of an IaC definition.
    """
    __tablename__ = "iac_templates"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    technology: Mapped[IaCTechnology] = mapped_column(Enum(IaCTechnology), default=IaCTechnology.UNKNOWN)
    repository_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IaCConfigurationFinding(Base):
    """
    Details a discovered misconfiguration in an IaC Template.
    """
    __tablename__ = "iac_findings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("iac_templates.id", ondelete="CASCADE"), index=True)
    
    severity: Mapped[str] = mapped_column(String(50), default="HIGH") # CRITICAL, HIGH, MEDIUM, LOW
    category: Mapped[str] = mapped_column(String(100), nullable=False) # NETWORK, IAM, STORAGE, ENCRYPTION
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # e.g. aws_s3_bucket.main
    line_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IaCPolicy(Base):
    """
    Codifies enterprise infrastructure constraints.
    """
    __tablename__ = "iac_policies"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IaCDeploymentGovernance(Base):
    """
    Tracks a specific pre-deployment rollout attempt and approval state.
    """
    __tablename__ = "iac_deployments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("iac_templates.id", ondelete="CASCADE"), index=True)
    
    status: Mapped[IaCDeploymentStatus] = mapped_column(Enum(IaCDeploymentStatus), default=IaCDeploymentStatus.PENDING_APPROVAL)
    
    requested_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class IaCGuidance(Base):
    """
    Captures AI-generated code fixes (e.g., HCL snippet replacements).
    """
    __tablename__ = "iac_guidance"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    finding_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("iac_findings.id", ondelete="CASCADE"), unique=True)
    
    suggested_code: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IaCAuditLog(Base):
    """
    Audit log for IaC deployments and policy changes.
    """
    __tablename__ = "iac_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

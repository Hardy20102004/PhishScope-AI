import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class AttackSurfaceNode(Base):
    __tablename__ = "mf_ctem_attack_surface"
    """
    Represents a public-facing or highly exposed entry point.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_id: Mapped[str] = mapped_column(String(255)) # ID from multi-cloud inventory
    asset_type: Mapped[str] = mapped_column(String(100))
    exposure_vector: Mapped[str] = mapped_column(String(100)) # PUBLIC_IP, EXPOSED_API, CREDENTIAL_LEAK
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class BusinessContextBoundary(Base):
    __tablename__ = "mf_ctem_business_context"
    """
    Maps cloud boundaries to business criticality.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    boundary_name: Mapped[str] = mapped_column(String(255)) # e.g. "Payment Processing VPC"
    boundary_type: Mapped[str] = mapped_column(String(100)) # VPC, NAMESPACE, RESOURCE_GROUP
    boundary_identifier: Mapped[str] = mapped_column(String(255)) 
    
    business_criticality: Mapped[str] = mapped_column(String(50)) # TIER_1, TIER_2, TIER_3
    compliance_scope: Mapped[str] = mapped_column(String(255), nullable=True) # PCI-DSS
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CloudExposureFinding(Base):
    __tablename__ = "mf_ctem_exposures"
    """
    A specific vulnerability, misconfiguration, or toxic combination.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    attack_surface_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ctem_attack_surface.id", ondelete="CASCADE"), index=True)
    finding_type: Mapped[str] = mapped_column(String(100)) # CVE, MISCONFIG, TOXIC_COMBO
    finding_name: Mapped[str] = mapped_column(String(255))
    
    raw_severity: Mapped[float] = mapped_column(Float) # Base CVSS or score
    contextual_risk_score: Mapped[float] = mapped_column(Float, default=0.0) # Calculated based on business context
    
    status: Mapped[str] = mapped_column(String(50), default="OPEN") # OPEN, IN_PROGRESS, REMEDIATED, ACCEPTED
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RemediationPlan(Base):
    __tablename__ = "mf_ctem_remediation_plans"
    """
    An AI-generated, prioritized roadmap to reduce exposure.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    exposure_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ctem_exposures.id", ondelete="CASCADE"), index=True)
    plan_title: Mapped[str] = mapped_column(String(255))
    
    steps: Mapped[dict] = mapped_column(JSON)
    estimated_risk_reduction: Mapped[float] = mapped_column(Float)
    
    governance_workflow_id: Mapped[uuid.UUID] = mapped_column(String(255), nullable=True) # Linked to mf_gov_workflows if automated
    status: Mapped[str] = mapped_column(String(50), default="PROPOSED")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

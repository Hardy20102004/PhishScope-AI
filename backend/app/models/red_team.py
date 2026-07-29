import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class RedTeamCampaign(Base):
    __tablename__ = "mf_rt_campaigns"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT") # DRAFT, PENDING_APPROVAL, AUTHORIZED, IN_PROGRESS, COMPLETED
    
    # JSON array defining in-scope and out-of-scope assets
    scope_definition: Mapped[dict] = mapped_column(JSON, default=dict) 
    
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    approvals = relationship("AuthorizationRecord", back_populates="campaign", cascade="all, delete-orphan")
    findings = relationship("CampaignFinding", back_populates="campaign", cascade="all, delete-orphan")


class AuthorizationRecord(Base):
    __tablename__ = "mf_rt_authorizations"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_rt_campaigns.id", ondelete="CASCADE"), index=True)
    
    stakeholder_role: Mapped[str] = mapped_column(String(100)) # e.g. CISO, LEGAL_COUNSEL
    stakeholder_id: Mapped[str] = mapped_column(String(255)) # email or UUID
    
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    signature_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    campaign = relationship("RedTeamCampaign", back_populates="approvals")


class CampaignFinding(Base):
    __tablename__ = "mf_rt_findings"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_rt_campaigns.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(50)) # LOW, MEDIUM, HIGH, CRITICAL
    tactic: Mapped[str] = mapped_column(String(100), nullable=True) # MITRE Mapping
    technique_id: Mapped[str] = mapped_column(String(50), nullable=True)
    
    is_remediated: Mapped[bool] = mapped_column(Boolean, default=False)
    
    campaign = relationship("RedTeamCampaign", back_populates="findings")

"""
PHOENIX X — Phase X-091
Enterprise Cyber Fusion Center, Cross-Domain Correlation & AI Security Intelligence Platform
Database Models
"""
import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey, Integer,
    String, Text, JSON, Enum
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

# ─────────────────────────────────────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────────────────────────────────────

class FusionRecordType(str, enum.Enum):
    CROSS_DOMAIN_THREAT = "CROSS_DOMAIN_THREAT"
    POSTURE_ANOMALY = "POSTURE_ANOMALY"
    STRATEGIC_RISK = "STRATEGIC_RISK"

class CyberRiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RecommendationStatus(str, enum.Enum):
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    IMPLEMENTED = "IMPLEMENTED"
    REJECTED = "REJECTED"


# ─────────────────────────────────────────────────────────────────────────────
# Cross-Domain Correlation
# ─────────────────────────────────────────────────────────────────────────────

class FusionRecord(Base):
    """
    Unified correlation object linking SOC alerts, DFIR investigations, identity anomalies, cloud risks, and AppSec findings.
    """
    __tablename__ = "cyber_fusion_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    record_type: Mapped[FusionRecordType] = mapped_column(Enum(FusionRecordType), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    source_modules: Mapped[List[str]] = mapped_column(JSON, default=list) # e.g. ["SOC", "ITDR", "CLOUD"]
    correlated_entities: Mapped[List[str]] = mapped_column(JSON, default=list) # e.g. ["user:david.smith", "aws:ec2:i-1234"]
    
    risk_level: Mapped[CyberRiskLevel] = mapped_column(Enum(CyberRiskLevel), default=CyberRiskLevel.LOW)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Executive Analytics & Risk
# ─────────────────────────────────────────────────────────────────────────────

class CrossDomainRiskScore(Base):
    """
    Aggregated enterprise risk index normalized across all security pillars.
    """
    __tablename__ = "cyber_fusion_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    enterprise_risk_index: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 100
    identity_risk_factor: Mapped[float] = mapped_column(Float, default=0.0)
    cloud_risk_factor: Mapped[float] = mapped_column(Float, default=0.0)
    appsec_risk_factor: Mapped[float] = mapped_column(Float, default=0.0)
    network_risk_factor: Mapped[float] = mapped_column(Float, default=0.0)
    
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# AI Decision Support
# ─────────────────────────────────────────────────────────────────────────────

class StrategicRecommendation(Base):
    """
    High-level AI-generated operational and strategic directives requiring human approval.
    """
    __tablename__ = "cyber_fusion_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    fusion_record_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("cyber_fusion_records.id", ondelete="SET NULL"), nullable=True)
    
    recommendation_text: Mapped[str] = mapped_column(Text, nullable=False)
    strategic_impact: Mapped[str] = mapped_column(Text, nullable=True)
    
    status: Mapped[RecommendationStatus] = mapped_column(Enum(RecommendationStatus), default=RecommendationStatus.PENDING_REVIEW)
    approved_by: Mapped[str] = mapped_column(String(255), nullable=True)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

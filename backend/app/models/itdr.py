"""
PHOENIX X — Phase X-084
Enterprise Identity Threat Detection & Response (ITDR) Platform
Database Models

Follows NIST SP 800-63, NIST SP 800-207.
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

class TelemetryEventType(str, enum.Enum):
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    MFA_CHALLENGE = "MFA_CHALLENGE"
    PASSWORD_RESET = "PASSWORD_RESET"
    SESSION_EVALUATION = "SESSION_EVALUATION"
    PRIVILEGE_ELEVATION = "PRIVILEGE_ELEVATION"
    ADMIN_ACTIVITY = "ADMIN_ACTIVITY"

class AttackType(str, enum.Enum):
    PASSWORD_SPRAY = "PASSWORD_SPRAY"
    CREDENTIAL_STUFFING = "CREDENTIAL_STUFFING"
    MFA_FATIGUE = "MFA_FATIGUE"
    IMPOSSIBLE_TRAVEL = "IMPOSSIBLE_TRAVEL"
    TOKEN_THEFT = "TOKEN_THEFT"
    PRIVILEGE_ABUSE = "PRIVILEGE_ABUSE"

class InvestigationStatus(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    MITIGATED = "MITIGATED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    CLOSED = "CLOSED"

class IdentityRiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NEGLIGIBLE = "NEGLIGIBLE"

class RecommendationAction(str, enum.Enum):
    REVOKE_SESSIONS = "REVOKE_SESSIONS"
    RESET_PASSWORD = "RESET_PASSWORD"
    REQUIRE_MFA = "REQUIRE_MFA"
    ISOLATE_ACCOUNT = "ISOLATE_ACCOUNT"
    NO_ACTION = "NO_ACTION"


# ─────────────────────────────────────────────────────────────────────────────
# Identity Telemetry
# ─────────────────────────────────────────────────────────────────────────────

class ITDRTelemetryEvent(Base):
    """
    Normalized identity telemetry (auth events, MFA, session changes).
    """
    __tablename__ = "itdr_telemetry_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    event_type: Mapped[TelemetryEventType] = mapped_column(Enum(TelemetryEventType), nullable=False, index=True)
    
    source_ip: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    device_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    app_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. SUCCESS, FAILURE
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Behavior Baseline
# ─────────────────────────────────────────────────────────────────────────────

class ITDRBehaviorBaseline(Base):
    """
    Behavioral profiles for identities.
    """
    __tablename__ = "itdr_behavior_baselines"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    frequent_ips: Mapped[List[str]] = mapped_column(JSON, default=list)
    frequent_locations: Mapped[List[str]] = mapped_column(JSON, default=list)
    frequent_devices: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    typical_active_hours: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    velocity_baseline: Mapped[float] = mapped_column(Float, default=0.0) # Average auth requests per hour
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Credential Attack Detections
# ─────────────────────────────────────────────────────────────────────────────

class ITDRCredentialAttack(Base):
    """
    Detected credential attacks.
    """
    __tablename__ = "itdr_credential_attacks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    attack_type: Mapped[AttackType] = mapped_column(Enum(AttackType), nullable=False, index=True)
    target_identities: Mapped[List[str]] = mapped_column(JSON, default=list) # Can target multiple if spraying
    
    source_ips: Mapped[List[str]] = mapped_column(JSON, default=list)
    event_count: Mapped[int] = mapped_column(Integer, default=1)
    
    severity: Mapped[IdentityRiskLevel] = mapped_column(Enum(IdentityRiskLevel), default=IdentityRiskLevel.HIGH)
    
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Investigations
# ─────────────────────────────────────────────────────────────────────────────

class ITDRInvestigation(Base):
    """
    Workspace for investigating identity threats.
    """
    __tablename__ = "itdr_investigations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    
    primary_identity: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    status: Mapped[InvestigationStatus] = mapped_column(Enum(InvestigationStatus), default=InvestigationStatus.NEW)
    
    linked_telemetry_ids: Mapped[List[str]] = mapped_column(JSON, default=list)
    linked_attack_ids: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    assigned_to: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Identity Risk Scores
# ─────────────────────────────────────────────────────────────────────────────

class ITDRRiskScore(Base):
    """
    Dynamic risk scores for identities based on behavior and telemetry.
    """
    __tablename__ = "itdr_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    auth_risk: Mapped[float] = mapped_column(Float, default=0.0)
    behavior_risk: Mapped[float] = mapped_column(Float, default=0.0)
    privilege_risk: Mapped[float] = mapped_column(Float, default=0.0)
    
    risk_level: Mapped[IdentityRiskLevel] = mapped_column(Enum(IdentityRiskLevel), default=IdentityRiskLevel.LOW)
    
    contributing_factors: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────────────────────────────────────

class ITDRRecommendation(Base):
    """
    Human-governed response recommendations.
    """
    __tablename__ = "itdr_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False)
    investigation_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("itdr_investigations.id", ondelete="SET NULL"), nullable=True)
    
    recommended_action: Mapped[RecommendationAction] = mapped_column(Enum(RecommendationAction), nullable=False)
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    
    action_taken: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

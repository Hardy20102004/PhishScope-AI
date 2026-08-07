"""
PHOENIX X — Phase X-081
Enterprise Identity Security Posture Management (ISPM) Platform
Database Models

Follows NIST SP 800-63, NIST SP 800-207 (Zero Trust), ISO/IEC 27001.
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

class IdentityType(str, enum.Enum):
    HUMAN = "HUMAN"
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"
    PRIVILEGED = "PRIVILEGED"
    MACHINE = "MACHINE"
    APPLICATION = "APPLICATION"
    API = "API"
    MANAGED_IDENTITY = "MANAGED_IDENTITY"
    WORKLOAD_IDENTITY = "WORKLOAD_IDENTITY"
    GUEST = "GUEST"
    BOT = "BOT"


class IdentityStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DORMANT = "DORMANT"
    DISABLED = "DISABLED"
    LOCKED = "LOCKED"
    ORPHANED = "ORPHANED"
    PENDING = "PENDING"


class IdentityProvider(str, enum.Enum):
    ENTRA_ID = "ENTRA_ID"
    ACTIVE_DIRECTORY = "ACTIVE_DIRECTORY"
    LDAP = "LDAP"
    OKTA = "OKTA"
    PING_IDENTITY = "PING_IDENTITY"
    FORGEROCK = "FORGEROCK"
    GOOGLE_CLOUD_IDENTITY = "GOOGLE_CLOUD_IDENTITY"
    AWS_IAM = "AWS_IAM"
    AZURE_RBAC = "AZURE_RBAC"
    GCP_IAM = "GCP_IAM"
    KUBERNETES_RBAC = "KUBERNETES_RBAC"
    ENTERPRISE_SSO = "ENTERPRISE_SSO"
    CUSTOM = "CUSTOM"


class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class FindingStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_REMEDIATION = "IN_REMEDIATION"
    RESOLVED = "RESOLVED"
    ACCEPTED_RISK = "ACCEPTED_RISK"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class AuthMethod(str, enum.Enum):
    PASSWORD = "PASSWORD"
    MFA_TOTP = "MFA_TOTP"
    MFA_PUSH = "MFA_PUSH"
    MFA_SMS = "MFA_SMS"
    MFA_HARDWARE_TOKEN = "MFA_HARDWARE_TOKEN"
    PASSKEY = "PASSKEY"
    CERTIFICATE = "CERTIFICATE"
    KERBEROS = "KERBEROS"
    SSO_SAML = "SSO_SAML"
    SSO_OIDC = "SSO_OIDC"
    PASSWORDLESS = "PASSWORDLESS"
    BIOMETRIC = "BIOMETRIC"


class RelationshipType(str, enum.Enum):
    MEMBER_OF = "MEMBER_OF"
    HAS_ROLE = "HAS_ROLE"
    OWNS_APP = "OWNS_APP"
    ACCESSES_RESOURCE = "ACCESSES_RESOURCE"
    DELEGATES_TO = "DELEGATES_TO"
    TRUSTS = "TRUSTS"
    HAS_PERMISSION = "HAS_PERMISSION"
    MANAGES = "MANAGES"
    REPORTS_TO = "REPORTS_TO"
    INHERITS_FROM = "INHERITS_FROM"


class RecommendationPriority(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ZeroTrustPillar(str, enum.Enum):
    IDENTITY = "IDENTITY"
    DEVICES = "DEVICES"
    NETWORKS = "NETWORKS"
    APPLICATIONS = "APPLICATIONS"
    DATA = "DATA"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    ANALYTICS = "ANALYTICS"


# ─────────────────────────────────────────────────────────────────────────────
# Identity Provider Registry
# ─────────────────────────────────────────────────────────────────────────────

class ISPMProviderRegistry(Base):
    """
    Registry of connected identity providers and platforms.
    Tracks connectivity health and sync status for each identity source.
    """
    __tablename__ = "ispm_provider_registry"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_type: Mapped[IdentityProvider] = mapped_column(Enum(IdentityProvider), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Connectivity
    endpoint_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_healthy: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sync_interval_minutes: Mapped[int] = mapped_column(Integer, default=60)

    # Inventory counts
    identity_count: Mapped[int] = mapped_column(Integer, default=0)
    group_count: Mapped[int] = mapped_column(Integer, default=0)
    role_count: Mapped[int] = mapped_column(Integer, default=0)
    permission_count: Mapped[int] = mapped_column(Integer, default=0)

    # Configuration
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    sync_scope: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Enterprise Identity Inventory
# ─────────────────────────────────────────────────────────────────────────────

class EnterpriseIdentity(Base):
    """
    Unified identity inventory across all connected identity platforms.
    Normalized representation of every human, service, machine, and API identity.
    """
    __tablename__ = "ispm_identities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    provider_registry_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ispm_provider_registry.id", ondelete="SET NULL"), nullable=True)

    # Core Identity Fields
    identity_type: Mapped[IdentityType] = mapped_column(Enum(IdentityType), nullable=False, index=True)
    source_provider: Mapped[IdentityProvider] = mapped_column(Enum(IdentityProvider), nullable=False, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)

    # Identity Attributes
    display_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    upn: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)  # User Principal Name
    email: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)
    department: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    manager_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ispm_identities.id", ondelete="SET NULL"), nullable=True)
    business_owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organizational_unit: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    # Lifecycle Status
    status: Mapped[IdentityStatus] = mapped_column(Enum(IdentityStatus), default=IdentityStatus.ACTIVE, index=True)
    is_privileged: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_federated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_guest: Mapped[bool] = mapped_column(Boolean, default=False)

    # Activity
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_activity_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    days_since_last_login: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    login_count_30d: Mapped[int] = mapped_column(Integer, default=0)

    # Risk Signals
    current_risk_score: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW, index=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    mfa_methods: Mapped[List[str]] = mapped_column(JSON, default=list)
    auth_methods: Mapped[List[str]] = mapped_column(JSON, default=list)
    has_privileged_access: Mapped[bool] = mapped_column(Boolean, default=False)
    privilege_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Metadata
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list)

    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Identity Groups
# ─────────────────────────────────────────────────────────────────────────────

class IdentityGroup(Base):
    """
    Enterprise group inventory. Groups are the primary vehicle for permission inheritance.
    Tracks nested group relationships and effective member counts.
    """
    __tablename__ = "ispm_groups"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    source_provider: Mapped[IdentityProvider] = mapped_column(Enum(IdentityProvider), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    group_type: Mapped[str] = mapped_column(String(100), default="SECURITY")  # SECURITY, DISTRIBUTION, DYNAMIC

    # Membership
    direct_member_count: Mapped[int] = mapped_column(Integer, default=0)
    effective_member_count: Mapped[int] = mapped_column(Integer, default=0)
    nested_group_count: Mapped[int] = mapped_column(Integer, default=0)

    # Risk
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    has_privileged_members: Mapped[bool] = mapped_column(Boolean, default=False)
    is_privileged_group: Mapped[bool] = mapped_column(Boolean, default=False)

    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Identity Roles
# ─────────────────────────────────────────────────────────────────────────────

class IdentityRole(Base):
    """
    Role inventory across cloud and enterprise IAM systems.
    Captures role definitions, permission boundaries, and assignment patterns.
    """
    __tablename__ = "ispm_roles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    source_provider: Mapped[IdentityProvider] = mapped_column(Enum(IdentityProvider), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    role_type: Mapped[str] = mapped_column(String(100), default="CUSTOM")  # BUILT_IN, CUSTOM, MANAGED

    # Scope
    scope: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    is_privileged_role: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_built_in: Mapped[bool] = mapped_column(Boolean, default=False)

    # Assignment metrics
    assignment_count: Mapped[int] = mapped_column(Integer, default=0)
    permission_count: Mapped[int] = mapped_column(Integer, default=0)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    unused_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Risk
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    privilege_score: Mapped[float] = mapped_column(Float, default=0.0)

    permissions: Mapped[List[str]] = mapped_column(JSON, default=list)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Identity Relationships (Graph Edges)
# ─────────────────────────────────────────────────────────────────────────────

class IdentityRelationship(Base):
    """
    Graph edges representing relationships between identity entities.
    Distinguished: OBSERVED (from discovery) vs INFERRED (from risk analysis).
    Enables shortest-path access path analysis and privilege escalation detection.
    """
    __tablename__ = "ispm_relationships"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)

    # Source Node
    source_entity_type: Mapped[str] = mapped_column(String(100), nullable=False)  # IDENTITY, GROUP, ROLE, APP, RESOURCE
    source_entity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    source_entity_name: Mapped[str] = mapped_column(String(512), nullable=False)

    # Target Node
    target_entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_entity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    target_entity_name: Mapped[str] = mapped_column(String(512), nullable=False)

    # Relationship
    relationship_type: Mapped[RelationshipType] = mapped_column(Enum(RelationshipType), nullable=False, index=True)
    is_observed: Mapped[bool] = mapped_column(Boolean, default=True)  # True=discovered, False=inferred
    is_direct: Mapped[bool] = mapped_column(Boolean, default=True)    # True=direct, False=inherited
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)

    # Risk context
    risk_weight: Mapped[float] = mapped_column(Float, default=0.0)
    is_privileged_path: Mapped[bool] = mapped_column(Boolean, default=False)

    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Identity Posture Assessments
# ─────────────────────────────────────────────────────────────────────────────

class IdentityPostureAssessment(Base):
    """
    Point-in-time posture assessment for a specific identity.
    Evaluates authentication strength, hygiene, privilege alignment, and compliance.
    """
    __tablename__ = "ispm_posture_assessments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ispm_identities.id", ondelete="CASCADE"), index=True)

    # Assessment Results
    overall_posture_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Authentication Assessment
    auth_strength_score: Mapped[float] = mapped_column(Float, default=0.0)
    mfa_compliant: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_method_strength: Mapped[str] = mapped_column(String(50), default="WEAK")  # WEAK, MODERATE, STRONG
    password_age_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    password_policy_compliant: Mapped[bool] = mapped_column(Boolean, default=True)
    sso_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    passwordless_capable: Mapped[bool] = mapped_column(Boolean, default=False)

    # Privilege Assessment
    privilege_score: Mapped[float] = mapped_column(Float, default=0.0)
    has_excess_permissions: Mapped[bool] = mapped_column(Boolean, default=False)
    unused_permission_count: Mapped[int] = mapped_column(Integer, default=0)
    privilege_creep_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    least_privilege_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Hygiene Assessment
    is_dormant: Mapped[bool] = mapped_column(Boolean, default=False)
    dormancy_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    has_orphaned_sessions: Mapped[bool] = mapped_column(Boolean, default=False)
    certificate_expiry_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Compliance
    nist_compliant: Mapped[bool] = mapped_column(Boolean, default=True)
    iso27001_compliant: Mapped[bool] = mapped_column(Boolean, default=True)
    zero_trust_compliant: Mapped[bool] = mapped_column(Boolean, default=False)

    findings: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    next_assessment_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Access Governance Findings
# ─────────────────────────────────────────────────────────────────────────────

class AccessGovernanceFinding(Base):
    """
    Access governance violations: SoD conflicts, excessive permissions,
    dormant privilege, policy gaps, and certification failures.
    """
    __tablename__ = "ispm_governance_findings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ispm_identities.id", ondelete="CASCADE"), nullable=True, index=True)

    finding_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # Types: SOD_CONFLICT, EXCESSIVE_PERMISSION, DORMANT_PRIVILEGE, POLICY_GAP,
    #        ORPHANED_ACCESS, ROLE_OVER_PROVISIONING, CERTIFICATION_OVERDUE,
    #        ADMIN_SPRAWL, SHARED_ACCOUNT, DELEGATED_ACCESS_RISK

    severity: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), nullable=False, index=True)
    status: Mapped[FindingStatus] = mapped_column(Enum(FindingStatus), default=FindingStatus.OPEN, index=True)

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    remediation_steps: Mapped[Text] = mapped_column(Text, nullable=True)

    # Affected entities
    affected_identity_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    affected_role_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    affected_resource: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    # Risk context
    business_impact: Mapped[str] = mapped_column(String(100), default="MEDIUM")
    compliance_frameworks: Mapped[List[str]] = mapped_column(JSON, default=list)

    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Authentication Assessments
# ─────────────────────────────────────────────────────────────────────────────

class AuthenticationAssessment(Base):
    """
    Tenant-wide authentication posture assessment.
    Tracks MFA adoption, SSO coverage, passwordless readiness, and method distribution.
    """
    __tablename__ = "ispm_auth_assessments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)

    # Coverage Metrics
    total_identities: Mapped[int] = mapped_column(Integer, default=0)
    mfa_enabled_count: Mapped[int] = mapped_column(Integer, default=0)
    mfa_coverage_pct: Mapped[float] = mapped_column(Float, default=0.0)
    sso_enabled_count: Mapped[int] = mapped_column(Integer, default=0)
    sso_coverage_pct: Mapped[float] = mapped_column(Float, default=0.0)
    passwordless_count: Mapped[int] = mapped_column(Integer, default=0)
    passwordless_coverage_pct: Mapped[float] = mapped_column(Float, default=0.0)

    # Method Distribution
    auth_method_distribution: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    mfa_method_distribution: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    # Risk Counts
    no_mfa_privileged_count: Mapped[int] = mapped_column(Integer, default=0)
    weak_auth_count: Mapped[int] = mapped_column(Integer, default=0)
    password_only_count: Mapped[int] = mapped_column(Integer, default=0)
    expired_certificates_count: Mapped[int] = mapped_column(Integer, default=0)

    # Scores
    overall_auth_score: Mapped[float] = mapped_column(Float, default=0.0)
    phishing_resistant_pct: Mapped[float] = mapped_column(Float, default=0.0)

    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Identity Risk Scores
# ─────────────────────────────────────────────────────────────────────────────

class IdentityRiskScore(Base):
    """
    Composite identity risk score.
    Combines authentication risk, privilege risk, behavioral signals,
    and threat intelligence to produce a holistic identity risk rating.
    Maintains historical trend data.
    """
    __tablename__ = "ispm_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ispm_identities.id", ondelete="CASCADE"), index=True)

    # Composite Score
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW, index=True)

    # Dimension Scores
    authentication_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    privilege_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    behavioral_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    hygiene_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    governance_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    threat_intel_risk_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Business Context
    business_criticality: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    operational_impact: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    zero_trust_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Confidence & Rationale
    confidence_score: Mapped[float] = mapped_column(Float, default=0.8)
    risk_rationale: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    contributing_factors: Mapped[List[str]] = mapped_column(JSON, default=list)

    # Trend
    score_delta_7d: Mapped[float] = mapped_column(Float, default=0.0)
    score_delta_30d: Mapped[float] = mapped_column(Float, default=0.0)
    trend: Mapped[str] = mapped_column(String(20), default="STABLE")  # IMPROVING, STABLE, WORSENING

    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# ISPM Recommendations
# ─────────────────────────────────────────────────────────────────────────────

class ISPMRecommendation(Base):
    """
    AI-generated, explainable identity security recommendations.
    Clearly distinguished: Observed Evidence → Calculated Metrics → Assessment → Recommendation.
    Aligned to NIST SP 800-63, NIST SP 800-207, and MITRE ATT&CK.
    """
    __tablename__ = "ispm_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ispm_identities.id", ondelete="SET NULL"), nullable=True)

    priority: Mapped[RecommendationPriority] = mapped_column(Enum(RecommendationPriority), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    # Categories: MFA_ENFORCEMENT, PRIVILEGE_REDUCTION, DORMANCY_CLEANUP,
    #             GOVERNANCE_REMEDIATION, AUTH_UPGRADE, ZERO_TRUST_IMPROVEMENT,
    #             COMPLIANCE_GAP, IDENTITY_HYGIENE

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    summary: Mapped[Text] = mapped_column(Text, nullable=False)

    # Explainable AI output — clearly separated layers
    observed_evidence: Mapped[List[str]] = mapped_column(JSON, default=list)
    calculated_metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    analytical_assessment: Mapped[Text] = mapped_column(Text, nullable=True)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)
    assumptions: Mapped[List[str]] = mapped_column(JSON, default=list)

    # Implementation guidance
    implementation_steps: Mapped[List[str]] = mapped_column(JSON, default=list)
    effort_estimate: Mapped[str] = mapped_column(String(50), default="MEDIUM")  # LOW, MEDIUM, HIGH
    expected_risk_reduction: Mapped[float] = mapped_column(Float, default=0.0)

    # Compliance alignment
    nist_controls: Mapped[List[str]] = mapped_column(JSON, default=list)
    mitre_techniques: Mapped[List[str]] = mapped_column(JSON, default=list)

    status: Mapped[FindingStatus] = mapped_column(Enum(FindingStatus), default=FindingStatus.OPEN, index=True)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Zero Trust Readiness Assessment
# ─────────────────────────────────────────────────────────────────────────────

class ZeroTrustReadinessAssessment(Base):
    """
    Zero Trust readiness measurement aligned to NIST SP 800-207.
    Scored per pillar: Identity, Devices, Networks, Applications, Data,
    Infrastructure, Analytics — then aggregated to an overall ZT score.
    """
    __tablename__ = "ispm_zt_readiness"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)

    # Overall Score
    overall_zt_score: Mapped[float] = mapped_column(Float, default=0.0)
    maturity_level: Mapped[str] = mapped_column(String(50), default="TRADITIONAL")
    # Levels: TRADITIONAL, INITIAL, ADVANCED, OPTIMAL

    # Per-Pillar Scores (NIST SP 800-207)
    identity_pillar_score: Mapped[float] = mapped_column(Float, default=0.0)
    devices_pillar_score: Mapped[float] = mapped_column(Float, default=0.0)
    networks_pillar_score: Mapped[float] = mapped_column(Float, default=0.0)
    applications_pillar_score: Mapped[float] = mapped_column(Float, default=0.0)
    data_pillar_score: Mapped[float] = mapped_column(Float, default=0.0)
    infrastructure_pillar_score: Mapped[float] = mapped_column(Float, default=0.0)
    analytics_pillar_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Identity-Specific ZT Criteria
    continuous_verification_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    least_privilege_enforced: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_everywhere: Mapped[bool] = mapped_column(Boolean, default=False)
    device_trust_required: Mapped[bool] = mapped_column(Boolean, default=False)
    session_risk_evaluated: Mapped[bool] = mapped_column(Boolean, default=False)
    privileged_access_workstations: Mapped[bool] = mapped_column(Boolean, default=False)

    gap_analysis: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    improvement_roadmap: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)

    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# ISPM Audit Log (Immutable)
# ─────────────────────────────────────────────────────────────────────────────

class ISPMAdminAuditLog(Base):
    """
    Immutable audit log for all ISPM platform administrative actions.
    Digitally signed entries for evidence integrity.
    Supports SOC2, ISO 27001, and NIST compliance requirements.
    """
    __tablename__ = "ispm_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(nullable=True)
    actor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    action: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    outcome: Mapped[str] = mapped_column(String(50), default="SUCCESS")
    ip_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Integrity
    entry_hash: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

"""
PHOENIX X — Phase X-081
Enterprise Identity Security Posture Management (ISPM) Platform
Pydantic Schemas — Full type-safe request/response contracts
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.ispm import (
    AuthMethod,
    FindingStatus,
    IdentityProvider,
    IdentityStatus,
    IdentityType,
    RecommendationPriority,
    RelationshipType,
    RiskLevel,
)


# ─────────────────────────────────────────────────────────────────────────────
# Provider Registry
# ─────────────────────────────────────────────────────────────────────────────

class ProviderRegistryBase(BaseModel):
    name: str
    provider_type: IdentityProvider
    display_name: Optional[str] = None
    description: Optional[str] = None
    endpoint_url: Optional[str] = None
    sync_interval_minutes: int = 60
    config: Dict[str, Any] = {}
    sync_scope: Dict[str, Any] = {}


class ProviderRegistryCreate(ProviderRegistryBase):
    pass


class ProviderRegistryResponse(ProviderRegistryBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    is_active: bool
    is_healthy: bool
    last_sync_at: Optional[datetime]
    identity_count: int
    group_count: int
    role_count: int
    permission_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Enterprise Identity
# ─────────────────────────────────────────────────────────────────────────────

class EnterpriseIdentityBase(BaseModel):
    identity_type: IdentityType
    source_provider: IdentityProvider
    external_id: Optional[str] = None
    display_name: str
    upn: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    business_owner: Optional[str] = None
    organizational_unit: Optional[str] = None
    status: IdentityStatus = IdentityStatus.ACTIVE
    is_privileged: bool = False
    is_federated: bool = False
    is_guest: bool = False
    mfa_enabled: bool = False
    mfa_methods: List[str] = []
    auth_methods: List[str] = []
    tags: List[str] = []
    metadata_json: Dict[str, Any] = {}


class EnterpriseIdentityCreate(EnterpriseIdentityBase):
    provider_registry_id: Optional[uuid.UUID] = None


class EnterpriseIdentityResponse(EnterpriseIdentityBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    provider_registry_id: Optional[uuid.UUID]
    current_risk_score: float
    risk_level: RiskLevel
    has_privileged_access: bool
    privilege_score: float
    last_login_at: Optional[datetime]
    last_activity_at: Optional[datetime]
    days_since_last_login: Optional[int]
    login_count_30d: int
    discovered_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Identity Group
# ─────────────────────────────────────────────────────────────────────────────

class IdentityGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    source_provider: IdentityProvider
    external_id: Optional[str] = None
    group_type: str = "SECURITY"
    owner: Optional[str] = None
    is_privileged_group: bool = False
    metadata_json: Dict[str, Any] = {}


class IdentityGroupCreate(IdentityGroupBase):
    pass


class IdentityGroupResponse(IdentityGroupBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    direct_member_count: int
    effective_member_count: int
    nested_group_count: int
    risk_level: RiskLevel
    has_privileged_members: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Identity Role
# ─────────────────────────────────────────────────────────────────────────────

class IdentityRoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    source_provider: IdentityProvider
    external_id: Optional[str] = None
    role_type: str = "CUSTOM"
    scope: Optional[str] = None
    is_privileged_role: bool = False
    is_built_in: bool = False
    permissions: List[str] = []
    metadata_json: Dict[str, Any] = {}


class IdentityRoleCreate(IdentityRoleBase):
    pass


class IdentityRoleResponse(IdentityRoleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    assignment_count: int
    permission_count: int
    last_used_at: Optional[datetime]
    unused_days: Optional[int]
    risk_level: RiskLevel
    privilege_score: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Identity Relationship
# ─────────────────────────────────────────────────────────────────────────────

class IdentityRelationshipBase(BaseModel):
    source_entity_type: str
    source_entity_id: str
    source_entity_name: str
    target_entity_type: str
    target_entity_id: str
    target_entity_name: str
    relationship_type: RelationshipType
    is_observed: bool = True
    is_direct: bool = True
    confidence_score: float = 1.0
    risk_weight: float = 0.0
    is_privileged_path: bool = False
    metadata_json: Dict[str, Any] = {}


class IdentityRelationshipCreate(IdentityRelationshipBase):
    pass


class IdentityRelationshipResponse(IdentityRelationshipBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Posture Assessment
# ─────────────────────────────────────────────────────────────────────────────

class IdentityPostureAssessmentResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: uuid.UUID
    overall_posture_score: float
    auth_strength_score: float
    mfa_compliant: bool
    mfa_method_strength: str
    password_age_days: Optional[int]
    password_policy_compliant: bool
    sso_enabled: bool
    passwordless_capable: bool
    privilege_score: float
    has_excess_permissions: bool
    unused_permission_count: int
    privilege_creep_detected: bool
    least_privilege_score: float
    is_dormant: bool
    dormancy_days: Optional[int]
    has_orphaned_sessions: bool
    certificate_expiry_days: Optional[int]
    nist_compliant: bool
    iso27001_compliant: bool
    zero_trust_compliant: bool
    findings: List[Dict[str, Any]]
    evidence: Dict[str, Any]
    assessed_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Access Governance Finding
# ─────────────────────────────────────────────────────────────────────────────

class AccessGovernanceFindingBase(BaseModel):
    finding_type: str
    severity: RiskLevel
    title: str
    description: str
    evidence: Dict[str, Any] = {}
    remediation_steps: Optional[str] = None
    affected_identity_name: Optional[str] = None
    affected_role_name: Optional[str] = None
    affected_resource: Optional[str] = None
    business_impact: str = "MEDIUM"
    compliance_frameworks: List[str] = []


class AccessGovernanceFindingCreate(AccessGovernanceFindingBase):
    identity_id: Optional[uuid.UUID] = None


class AccessGovernanceFindingResponse(AccessGovernanceFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: Optional[uuid.UUID]
    status: FindingStatus
    detected_at: datetime
    resolved_at: Optional[datetime]
    due_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Authentication Assessment
# ─────────────────────────────────────────────────────────────────────────────

class AuthenticationAssessmentResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    total_identities: int
    mfa_enabled_count: int
    mfa_coverage_pct: float
    sso_enabled_count: int
    sso_coverage_pct: float
    passwordless_count: int
    passwordless_coverage_pct: float
    auth_method_distribution: Dict[str, Any]
    mfa_method_distribution: Dict[str, Any]
    no_mfa_privileged_count: int
    weak_auth_count: int
    password_only_count: int
    expired_certificates_count: int
    overall_auth_score: float
    phishing_resistant_pct: float
    assessed_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Identity Risk Score
# ─────────────────────────────────────────────────────────────────────────────

class IdentityRiskScoreResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: uuid.UUID
    overall_score: float
    risk_level: RiskLevel
    authentication_risk_score: float
    privilege_risk_score: float
    behavioral_risk_score: float
    hygiene_risk_score: float
    governance_risk_score: float
    threat_intel_risk_score: float
    business_criticality: str
    operational_impact: str
    zero_trust_readiness_score: float
    confidence_score: float
    risk_rationale: Dict[str, Any]
    contributing_factors: List[str]
    score_delta_7d: float
    score_delta_30d: float
    trend: str
    calculated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# ISPM Recommendation
# ─────────────────────────────────────────────────────────────────────────────

class ISPMRecommendationBase(BaseModel):
    priority: RecommendationPriority
    category: str
    title: str
    summary: str
    observed_evidence: List[str] = []
    calculated_metrics: Dict[str, Any] = {}
    analytical_assessment: Optional[str] = None
    recommendation: str
    assumptions: List[str] = []
    implementation_steps: List[str] = []
    effort_estimate: str = "MEDIUM"
    expected_risk_reduction: float = 0.0
    nist_controls: List[str] = []
    mitre_techniques: List[str] = []


class ISPMRecommendationCreate(ISPMRecommendationBase):
    identity_id: Optional[uuid.UUID] = None


class ISPMRecommendationResponse(ISPMRecommendationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: Optional[uuid.UUID]
    status: FindingStatus
    is_ai_generated: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Zero Trust Readiness
# ─────────────────────────────────────────────────────────────────────────────

class ZeroTrustReadinessResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    overall_zt_score: float
    maturity_level: str
    identity_pillar_score: float
    devices_pillar_score: float
    networks_pillar_score: float
    applications_pillar_score: float
    data_pillar_score: float
    infrastructure_pillar_score: float
    analytics_pillar_score: float
    continuous_verification_enabled: bool
    least_privilege_enforced: bool
    mfa_everywhere: bool
    device_trust_required: bool
    session_risk_evaluated: bool
    privileged_access_workstations: bool
    gap_analysis: List[Dict[str, Any]]
    improvement_roadmap: List[Dict[str, Any]]
    assessed_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard Summary Schemas
# ─────────────────────────────────────────────────────────────────────────────

class ISPMDashboardSummary(BaseModel):
    """Executive-level ISPM posture overview."""
    # Identity Counts
    total_identities: int
    human_identities: int
    service_accounts: int
    machine_identities: int
    privileged_identities: int
    dormant_identities: int
    orphaned_identities: int

    # Authentication Posture
    mfa_coverage_pct: float
    sso_coverage_pct: float
    passwordless_pct: float
    privileged_no_mfa_count: int

    # Risk Distribution
    critical_risk_identities: int
    high_risk_identities: int
    medium_risk_identities: int
    low_risk_identities: int
    average_risk_score: float

    # Governance
    open_governance_findings: int
    critical_governance_findings: int
    sod_violations: int
    excess_permission_count: int

    # Zero Trust
    zero_trust_score: float
    zero_trust_maturity: str

    # Compliance
    nist_compliance_pct: float
    iso27001_compliance_pct: float

    # Recommendations
    critical_recommendations: int
    total_recommendations: int


class ISPMIdentityDetail(BaseModel):
    """Full identity detail including risk, posture, relationships."""
    identity: EnterpriseIdentityResponse
    risk_score: Optional[IdentityRiskScoreResponse]
    posture_assessment: Optional[IdentityPostureAssessmentResponse]
    governance_findings: List[AccessGovernanceFindingResponse]
    recommendations: List[ISPMRecommendationResponse]
    relationships: List[IdentityRelationshipResponse]


class AIAssistantRequest(BaseModel):
    query: str
    context_identity_ids: Optional[List[uuid.UUID]] = None
    include_executive_summary: bool = True
    include_recommendations: bool = True
    analysis_mode: str = "COMPREHENSIVE"  # COMPREHENSIVE, QUICK, FOCUSED


class AIAssistantResponse(BaseModel):
    query: str
    identity_security_summary: str
    access_governance_summary: str
    authentication_summary: str
    risk_summary: str
    zero_trust_readiness_report: str
    executive_summary: str
    prioritized_roadmap: List[Dict[str, Any]]
    observed_evidence: List[str]
    calculated_metrics: Dict[str, Any]
    analytical_assessment: str
    recommendations: List[str]
    assumptions: List[str]
    confidence_score: float
    generated_at: datetime

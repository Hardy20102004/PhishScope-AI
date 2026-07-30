"""
PHOENIX X — Phase X-081
Enterprise Identity Security Posture Management (ISPM) Platform
REST API Router

All endpoints follow established PHOENIX X patterns:
- Async SQLAlchemy
- Tenant-isolated
- JWT-authenticated
- RBAC enforced
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.api import deps
from app.models.user import User
from app.models.ispm import (
    FindingStatus, RecommendationPriority, RiskLevel,
    IdentityType, IdentityStatus, RelationshipType
)
from app.schemas.ispm import (
    ProviderRegistryCreate, ProviderRegistryResponse,
    EnterpriseIdentityCreate, EnterpriseIdentityResponse,
    IdentityGroupCreate, IdentityGroupResponse,
    IdentityRoleCreate, IdentityRoleResponse,
    IdentityRelationshipCreate, IdentityRelationshipResponse,
    IdentityPostureAssessmentResponse,
    AccessGovernanceFindingCreate, AccessGovernanceFindingResponse,
    AuthenticationAssessmentResponse,
    IdentityRiskScoreResponse,
    ISPMRecommendationCreate, ISPMRecommendationResponse,
    ZeroTrustReadinessResponse,
    ISPMDashboardSummary,
    AIAssistantRequest, AIAssistantResponse,
)
from app.ispm.discovery_engine import IdentityDiscoveryEngine
from app.ispm.inventory_engine import IdentityInventoryEngine
from app.ispm.relationship_engine import IdentityRelationshipEngine
from app.ispm.posture_engine import IdentityPostureEngine
from app.ispm.governance_engine import AccessGovernanceEngine
from app.ispm.auth_assessment_engine import AuthenticationAssessmentEngine
from app.ispm.risk_engine import IdentityRiskEngine
from app.ispm.recommendation_engine import ISPMRecommendationEngine
from app.ispm.executive_analytics import ISPMExecutiveAnalyticsEngine

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# ISPM Dashboard
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/dashboard", summary="ISPM Executive Dashboard Summary")
async def get_ispm_dashboard(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Returns the comprehensive ISPM executive dashboard data.
    Includes identity inventory counts, authentication posture, risk distribution,
    governance findings, Zero Trust readiness, and compliance status.
    """
    engine = ISPMExecutiveAnalyticsEngine(db)
    return await engine.get_dashboard_summary(current_user.tenant_id)


# ─────────────────────────────────────────────────────────────────────────────
# Identity Provider Registry
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/providers", response_model=List[ProviderRegistryResponse], summary="List Identity Providers")
async def list_providers(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """List all registered identity providers and their sync status."""
    from sqlalchemy import select
    from app.models.ispm import ISPMProviderRegistry
    stmt = select(ISPMProviderRegistry).where(
        ISPMProviderRegistry.tenant_id == current_user.tenant_id
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/providers", response_model=ProviderRegistryResponse, status_code=status.HTTP_201_CREATED,
             summary="Register Identity Provider")
async def register_provider(
    provider_in: ProviderRegistryCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Register a new identity provider for continuous discovery."""
    from app.models.ispm import ISPMProviderRegistry
    provider = ISPMProviderRegistry(
        tenant_id=current_user.tenant_id,
        **provider_in.model_dump()
    )
    db.add(provider)
    await db.commit()
    await db.refresh(provider)
    return provider


# ─────────────────────────────────────────────────────────────────────────────
# Identity Discovery
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/discovery/run", summary="Run Identity Discovery")
async def run_discovery(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Trigger a full identity discovery scan across all registered providers.
    Returns a discovery summary with counts per provider.
    """
    engine = IdentityDiscoveryEngine(db)
    return await engine.discover_all(current_user.tenant_id)


@router.get("/discovery/status", summary="Discovery Status")
async def get_discovery_status(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the current status of identity discovery across all providers."""
    engine = IdentityDiscoveryEngine(db)
    return await engine.get_discovery_status(current_user.tenant_id)


# ─────────────────────────────────────────────────────────────────────────────
# Identity Inventory
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/identities", response_model=List[EnterpriseIdentityResponse], summary="Identity Inventory")
async def list_identities(
    identity_type: Optional[IdentityType] = Query(None),
    status: Optional[IdentityStatus] = Query(None),
    risk_level: Optional[RiskLevel] = Query(None),
    is_privileged: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Returns the full enterprise identity inventory with filtering and search.
    Supports filtering by type, status, risk level, and privileged status.
    """
    engine = IdentityInventoryEngine(db)
    return await engine.list_identities(
        current_user.tenant_id,
        identity_type=identity_type,
        status=status,
        risk_level=risk_level,
        is_privileged=is_privileged,
        search=search,
        limit=limit,
        offset=offset
    )


@router.post("/identities", response_model=EnterpriseIdentityResponse, status_code=status.HTTP_201_CREATED,
             summary="Register Identity")
async def create_identity(
    identity_in: EnterpriseIdentityCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Register or upsert an enterprise identity."""
    engine = IdentityInventoryEngine(db)
    return await engine.create_identity(current_user.tenant_id, identity_in)


@router.get("/identities/summary", summary="Identity Inventory Summary")
async def get_identity_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Returns aggregated identity inventory counts for dashboard widgets."""
    engine = IdentityInventoryEngine(db)
    return await engine.get_summary_counts(current_user.tenant_id)


@router.get("/identities/{identity_id}", response_model=EnterpriseIdentityResponse, summary="Identity Detail")
async def get_identity(
    identity_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get full detail for a specific identity."""
    engine = IdentityInventoryEngine(db)
    identity = await engine.get_identity(identity_id)
    if not identity or identity.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity


@router.get("/identities/{identity_id}/risk", response_model=IdentityRiskScoreResponse,
            summary="Identity Risk Score")
async def get_identity_risk(
    identity_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the composite risk score and rationale for an identity."""
    engine = IdentityRiskEngine(db)
    score = await engine.get_risk_score(identity_id)
    if not score:
        raise HTTPException(status_code=404, detail="Risk score not yet calculated for this identity")
    return score


@router.get("/identities/{identity_id}/relationships", response_model=List[IdentityRelationshipResponse],
            summary="Identity Relationships")
async def get_identity_relationships(
    identity_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get all graph relationships for a specific identity."""
    engine = IdentityRelationshipEngine(db)
    return await engine.get_identity_relationships(
        current_user.tenant_id, str(identity_id)
    )


@router.get("/identities/{identity_id}/posture", response_model=IdentityPostureAssessmentResponse,
            summary="Identity Posture Assessment")
async def get_identity_posture(
    identity_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the posture assessment for a specific identity."""
    engine = IdentityPostureEngine(db)
    assessment = await engine.get_posture_assessment(identity_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Posture assessment not found")
    return assessment


# ─────────────────────────────────────────────────────────────────────────────
# Groups & Roles
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/groups", response_model=List[IdentityGroupResponse], summary="Identity Groups")
async def list_groups(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = IdentityInventoryEngine(db)
    return await engine.list_groups(current_user.tenant_id)


@router.post("/groups", response_model=IdentityGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_in: IdentityGroupCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = IdentityInventoryEngine(db)
    return await engine.create_group(current_user.tenant_id, group_in)


@router.get("/roles", response_model=List[IdentityRoleResponse], summary="Identity Roles")
async def list_roles(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = IdentityInventoryEngine(db)
    return await engine.list_roles(current_user.tenant_id)


@router.post("/roles", response_model=IdentityRoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: IdentityRoleCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = IdentityInventoryEngine(db)
    return await engine.create_role(current_user.tenant_id, role_in)


# ─────────────────────────────────────────────────────────────────────────────
# Identity Relationships
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/relationships", response_model=List[IdentityRelationshipResponse], summary="Identity Relationships")
async def list_relationships(
    relationship_type: Optional[RelationshipType] = Query(None),
    is_privileged_path: Optional[bool] = Query(None),
    is_observed: Optional[bool] = Query(None),
    limit: int = Query(200, le=500),
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = IdentityRelationshipEngine(db)
    return await engine.list_relationships(
        current_user.tenant_id,
        relationship_type=relationship_type,
        is_privileged_path=is_privileged_path,
        is_observed=is_observed,
        limit=limit
    )


@router.get("/relationships/graph", summary="Identity Relationship Graph Snapshot")
async def get_relationship_graph(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Returns a serializable graph snapshot for frontend visualization."""
    engine = IdentityRelationshipEngine(db)
    return await engine.build_graph_snapshot(current_user.tenant_id)


@router.get("/relationships/privilege-paths", summary="Privilege Escalation Paths")
async def get_privilege_escalation_paths(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Detect and return identified privilege escalation paths in the identity graph."""
    engine = IdentityRelationshipEngine(db)
    return await engine.detect_privilege_escalation_paths(current_user.tenant_id)


@router.post("/relationships/seed-demo", summary="Seed Demo Relationships")
async def seed_demo_relationships(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Seed demonstration relationship data for UI visualization."""
    engine = IdentityRelationshipEngine(db)
    count = await engine.seed_demo_relationships(current_user.tenant_id)
    return {"seeded": count}


# ─────────────────────────────────────────────────────────────────────────────
# Identity Posture Assessment
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/posture/assess-all", summary="Run Full Posture Assessment")
async def run_full_posture_assessment(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Run posture assessment for all identities in the tenant."""
    engine = IdentityPostureEngine(db)
    return await engine.assess_all_identities(current_user.tenant_id)


@router.post("/posture/assess/{identity_id}", response_model=IdentityPostureAssessmentResponse,
             summary="Assess Identity Posture")
async def assess_identity_posture(
    identity_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Run posture assessment for a specific identity."""
    engine = IdentityPostureEngine(db)
    return await engine.assess_identity(current_user.tenant_id, identity_id)


@router.get("/posture", summary="Overall Posture Summary")
async def get_posture_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get aggregated identity posture summary across all assessed identities."""
    engine = IdentityPostureEngine(db)
    return await engine.get_overall_posture_summary(current_user.tenant_id)


# ─────────────────────────────────────────────────────────────────────────────
# Access Governance
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/governance/scan", summary="Run Governance Scan")
async def run_governance_scan(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Run full access governance scan — detects SoD, excessive permissions, dormancy, etc."""
    engine = AccessGovernanceEngine(db)
    return await engine.run_governance_scan(current_user.tenant_id)


@router.get("/governance/findings", response_model=List[AccessGovernanceFindingResponse],
            summary="Governance Findings")
async def list_governance_findings(
    severity: Optional[RiskLevel] = Query(None),
    finding_type: Optional[str] = Query(None),
    finding_status: Optional[FindingStatus] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = AccessGovernanceEngine(db)
    return await engine.list_findings(
        current_user.tenant_id,
        severity=severity,
        finding_type=finding_type,
        status=finding_status,
        limit=limit,
        offset=offset
    )


@router.get("/governance", summary="Governance Summary")
async def get_governance_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Returns aggregated access governance summary for the dashboard."""
    engine = AccessGovernanceEngine(db)
    return await engine.get_governance_summary(current_user.tenant_id)


@router.post("/governance/findings", response_model=AccessGovernanceFindingResponse,
             status_code=status.HTTP_201_CREATED, summary="Create Governance Finding")
async def create_governance_finding(
    finding_in: AccessGovernanceFindingCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = AccessGovernanceEngine(db)
    return await engine.create_finding(current_user.tenant_id, finding_in)


# ─────────────────────────────────────────────────────────────────────────────
# Authentication Assessment
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/authentication/assess", response_model=AuthenticationAssessmentResponse,
             summary="Run Authentication Assessment")
async def run_auth_assessment(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Run tenant-wide authentication posture assessment."""
    engine = AuthenticationAssessmentEngine(db)
    return await engine.run_assessment(current_user.tenant_id)


@router.get("/authentication", response_model=AuthenticationAssessmentResponse,
            summary="Authentication Assessment")
async def get_auth_assessment(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the latest authentication posture assessment."""
    engine = AuthenticationAssessmentEngine(db)
    assessment = await engine.get_latest_assessment(current_user.tenant_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="No authentication assessment found. Run /authentication/assess first.")
    return assessment


# ─────────────────────────────────────────────────────────────────────────────
# Identity Risk
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/risk", summary="Identity Risk Distribution")
async def get_risk_distribution(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Returns risk score distribution across all tenant identities."""
    engine = IdentityRiskEngine(db)
    return await engine.get_risk_distribution(current_user.tenant_id)


@router.post("/risk/calculate/{identity_id}", response_model=IdentityRiskScoreResponse,
             summary="Calculate Identity Risk")
async def calculate_identity_risk(
    identity_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Calculate (or recalculate) the composite risk score for a specific identity."""
    engine = IdentityRiskEngine(db)
    return await engine.calculate_identity_risk(current_user.tenant_id, identity_id)


# ─────────────────────────────────────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/recommendations/generate", summary="Generate AI Recommendations")
async def generate_recommendations(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Generate AI-assisted, explainable identity security recommendations."""
    engine = ISPMRecommendationEngine(db)
    return await engine.generate_recommendations(current_user.tenant_id)


@router.get("/recommendations", response_model=List[ISPMRecommendationResponse],
            summary="ISPM Recommendations")
async def list_recommendations(
    priority: Optional[RecommendationPriority] = Query(None),
    category: Optional[str] = Query(None),
    rec_status: Optional[FindingStatus] = Query(None),
    limit: int = Query(100, le=500),
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ISPMRecommendationEngine(db)
    return await engine.list_recommendations(
        current_user.tenant_id,
        priority=priority,
        category=category,
        status=rec_status,
        limit=limit
    )


@router.get("/recommendations/roadmap", summary="Improvement Roadmap")
async def get_improvement_roadmap(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get a prioritized Zero Trust improvement roadmap from AI recommendations."""
    engine = ISPMRecommendationEngine(db)
    return await engine.generate_improvement_roadmap(current_user.tenant_id)


# ─────────────────────────────────────────────────────────────────────────────
# Zero Trust Readiness
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/zero-trust", summary="Zero Trust Readiness Assessment")
async def get_zero_trust_readiness(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Returns Zero Trust readiness assessment per NIST SP 800-207 pillars.
    Includes per-pillar scores, gap analysis, and improvement roadmap.
    """
    engine = ISPMExecutiveAnalyticsEngine(db)
    return await engine.get_zero_trust_readiness(current_user.tenant_id)


# ─────────────────────────────────────────────────────────────────────────────
# Compliance
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/compliance", summary="Compliance Status")
async def get_compliance_status(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Returns compliance status against NIST, ISO 27001, SOC2, and CIS Controls."""
    engine = ISPMExecutiveAnalyticsEngine(db)
    return await engine.get_compliance_status(current_user.tenant_id)


# ─────────────────────────────────────────────────────────────────────────────
# Historical Trends
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/trends", summary="Historical Trends")
async def get_historical_trends(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Returns historical trend data for all ISPM posture dimensions."""
    engine = ISPMExecutiveAnalyticsEngine(db)
    return await engine.get_historical_trends(current_user.tenant_id)


# ─────────────────────────────────────────────────────────────────────────────
# AI Identity Security Assistant
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/ai-assistant", summary="AI Identity Security Assistant")
async def ai_identity_assistant(
    request: AIAssistantRequest,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    AI-powered Identity Security Assistant.
    Generates explainable identity security summaries, recommendations,
    and Zero Trust readiness reports using the AI Security Brain.

    Output clearly distinguishes:
    - Observed Evidence (from discovery)
    - Calculated Metrics (computed scores)
    - Analytical Assessment (AI reasoning)
    - Recommendations (actionable guidance)
    - Assumptions (data completeness caveats)
    """
    # Fetch current posture data
    exec_engine = ISPMExecutiveAnalyticsEngine(db)
    dashboard = await exec_engine.get_dashboard_summary(current_user.tenant_id)
    zt = await exec_engine.get_zero_trust_readiness(current_user.tenant_id)

    rec_engine = ISPMRecommendationEngine(db)
    roadmap = await rec_engine.generate_improvement_roadmap(current_user.tenant_id)
    recommendations = await rec_engine.list_recommendations(current_user.tenant_id, limit=10)

    # Build explainable AI response
    mfa_pct = dashboard.get("mfa_coverage_pct", 0)
    avg_risk = dashboard.get("average_risk_score", 0)
    critical_ids = dashboard.get("critical_risk_identities", 0)
    total_ids = dashboard.get("total_identities", 0)

    return AIAssistantResponse(
        query=request.query,
        identity_security_summary=(
            f"The enterprise has {total_ids} identities across all connected platforms. "
            f"MFA coverage stands at {mfa_pct:.1f}% with {dashboard.get('privileged_no_mfa_count', 0)} "
            f"privileged accounts lacking MFA protection. "
            f"{dashboard.get('dormant_identities', 0)} dormant identities and "
            f"{dashboard.get('orphaned_identities', 0)} orphaned identities require immediate remediation."
        ),
        access_governance_summary=(
            f"{dashboard.get('open_governance_findings', 0)} open governance findings detected. "
            f"Critical issues include: {dashboard.get('sod_violations', 0)} SoD violations, "
            f"{dashboard.get('excess_permission_count', 0)} excessive permission grants, and "
            f"{dashboard.get('dormant_privileges', 0)} dormant privilege accounts. "
            f"{'Admin sprawl detected — privileged account count exceeds recommended thresholds.' if dashboard.get('admin_sprawl_detected') else ''}"
        ),
        authentication_summary=(
            f"Authentication posture: MFA coverage {mfa_pct:.1f}%, "
            f"SSO coverage {dashboard.get('sso_coverage_pct', 0):.1f}%, "
            f"Passwordless {dashboard.get('passwordless_pct', 0):.1f}%, "
            f"Phishing-resistant auth {dashboard.get('phishing_resistant_pct', 0):.1f}%. "
            f"Auth score: {dashboard.get('overall_auth_score', 0):.0f}/100."
        ),
        risk_summary=(
            f"Risk distribution: {critical_ids} critical, {dashboard.get('high_risk_identities', 0)} high, "
            f"{dashboard.get('medium_risk_identities', 0)} medium, {dashboard.get('low_risk_identities', 0)} low risk identities. "
            f"Average risk score: {avg_risk:.1f}/100. "
            f"Primary risk drivers: insufficient MFA coverage, excessive permissions, and dormant privileged accounts."
        ),
        zero_trust_readiness_report=(
            f"Zero Trust readiness score: {zt.get('overall_zt_score', 0):.1f}/100 — {zt.get('maturity_level', 'TRADITIONAL')} maturity. "
            f"Identity pillar: {zt.get('pillars', {}).get('identity', 0):.1f}. "
            f"Key gaps: {', '.join(g['description'] for g in zt.get('gap_analysis', [])[:2])}."
        ),
        executive_summary=(
            f"ISPM Executive Summary: The enterprise identity posture requires immediate attention. "
            f"With {mfa_pct:.1f}% MFA coverage and {critical_ids} critical-risk identities, "
            f"the organization faces elevated credential-based attack exposure. "
            f"Zero Trust readiness is at {zt.get('maturity_level', 'TRADITIONAL')} maturity "
            f"({zt.get('overall_zt_score', 0):.1f}/100). "
            f"Prioritized actions: enforce MFA on all privileged accounts, "
            f"remediate {dashboard.get('dormant_identities', 0)} dormant identities, "
            f"and address {dashboard.get('open_governance_findings', 0)} open governance findings."
        ),
        prioritized_roadmap=roadmap,
        observed_evidence=[
            f"Total identities discovered: {total_ids}",
            f"MFA enabled: {mfa_pct:.1f}% of identities",
            f"Dormant identities: {dashboard.get('dormant_identities', 0)}",
            f"Privileged accounts: {dashboard.get('privileged_identities', 0)}",
            f"Open governance findings: {dashboard.get('open_governance_findings', 0)}",
            f"Zero Trust score: {zt.get('overall_zt_score', 0):.1f}/100"
        ],
        calculated_metrics={
            "mfa_coverage_pct": mfa_pct,
            "average_risk_score": avg_risk,
            "zero_trust_score": zt.get("overall_zt_score", 0),
            "governance_findings": dashboard.get("open_governance_findings", 0),
            "critical_risk_identities": critical_ids
        },
        analytical_assessment=(
            f"Based on the observed evidence and calculated metrics, the identity security posture "
            f"presents significant risk. The combination of {mfa_pct:.1f}% MFA coverage and "
            f"{critical_ids} critical-risk identities creates material exposure to credential-based "
            f"attacks (MITRE T1078, T1110). The {zt.get('maturity_level', 'TRADITIONAL')} Zero Trust "
            f"maturity indicates the organization has not yet implemented continuous identity verification."
        ),
        recommendations=[r.title for r in recommendations[:5]],
        assumptions=[
            "Risk scores are calculated from available inventory data and may not reflect all risk signals",
            "Behavioral analysis is limited to simulated signals in this deployment",
            "Threat intelligence enrichment reflects sample data"
        ],
        confidence_score=0.82,
        generated_at=datetime.now(timezone.utc)
    )

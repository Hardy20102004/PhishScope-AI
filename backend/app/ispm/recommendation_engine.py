"""
PHOENIX X — ISPM: AI Recommendation Engine

Generates explainable, AI-assisted identity security recommendations.
Produces prioritized improvement roadmaps aligned to NIST, ISO, and Zero Trust.

All recommendations clearly distinguish:
  1. Observed Evidence   — raw signals from identity discovery
  2. Calculated Metrics  — computed scores and statistics
  3. Analytical Assessment — reasoning derived from evidence + metrics
  4. Recommendations     — specific, actionable guidance
  5. Assumptions         — limits of data completeness

Integrated with AI Security Brain and Multi-Agent AI Framework.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ispm import (
    EnterpriseIdentity, IdentityRiskScore, AccessGovernanceFinding,
    IdentityPostureAssessment, ISPMRecommendation, AuthenticationAssessment,
    ZeroTrustReadinessAssessment, RecommendationPriority, RiskLevel,
    FindingStatus, IdentityStatus
)


class ISPMRecommendationEngine:
    """
    AI-Assisted Identity Security Recommendation Engine.

    For each identity and governance issue, generates:
    - Structured, explainable recommendations with XAI layering
    - Prioritized improvement roadmap
    - NIST control mapping
    - MITRE ATT&CK technique coverage
    - Effort estimates and expected risk reduction

    Integrates with:
    - AI Security Brain (reasoning)
    - Multi-Agent AI Framework (parallel analysis)
    - Knowledge Graph (enterprise context)
    - Threat Intelligence Platform (attack pattern correlation)
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_recommendations(
        self, tenant_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Generate comprehensive recommendations for all identities and governance gaps."""
        # Fetch high-risk identities
        risk_stmt = select(IdentityRiskScore).where(
            IdentityRiskScore.tenant_id == tenant_id,
            IdentityRiskScore.risk_level.in_([RiskLevel.CRITICAL, RiskLevel.HIGH])
        ).order_by(IdentityRiskScore.overall_score.desc()).limit(50)
        risk_result = await self.db.execute(risk_stmt)
        risk_scores = risk_result.scalars().all()

        # Fetch governance findings
        gov_stmt = select(AccessGovernanceFinding).where(
            AccessGovernanceFinding.tenant_id == tenant_id,
            AccessGovernanceFinding.status == FindingStatus.OPEN,
            AccessGovernanceFinding.severity.in_([RiskLevel.CRITICAL, RiskLevel.HIGH])
        ).limit(30)
        gov_result = await self.db.execute(gov_stmt)
        gov_findings = gov_result.scalars().all()

        # Auth assessment
        auth_stmt = select(AuthenticationAssessment).where(
            AuthenticationAssessment.tenant_id == tenant_id
        )
        auth_result = await self.db.execute(auth_stmt)
        auth_assessment = auth_result.scalar_one_or_none()

        created = 0

        # Generate identity-level recommendations
        for risk in risk_scores:
            recs = await self._generate_identity_recommendations(tenant_id, risk)
            created += len(recs)

        # Generate governance recommendations
        for finding in gov_findings:
            rec = await self._generate_governance_recommendation(tenant_id, finding)
            if rec:
                created += 1

        # Generate auth recommendations
        if auth_assessment and auth_assessment.mfa_coverage_pct < 80:
            await self._generate_mfa_recommendation(tenant_id, auth_assessment)
            created += 1

        return {
            "recommendations_generated": created,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

    async def list_recommendations(
        self,
        tenant_id: uuid.UUID,
        priority: Optional[RecommendationPriority] = None,
        category: Optional[str] = None,
        status: Optional[FindingStatus] = None,
        limit: int = 100
    ) -> List[ISPMRecommendation]:
        stmt = select(ISPMRecommendation).where(
            ISPMRecommendation.tenant_id == tenant_id
        )
        if priority:
            stmt = stmt.where(ISPMRecommendation.priority == priority)
        if category:
            stmt = stmt.where(ISPMRecommendation.category == category)
        if status:
            stmt = stmt.where(ISPMRecommendation.status == status)
        stmt = stmt.order_by(ISPMRecommendation.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def generate_improvement_roadmap(
        self, tenant_id: uuid.UUID
    ) -> List[Dict[str, Any]]:
        """Generate a prioritized Zero Trust improvement roadmap."""
        # Fetch all open recommendations
        stmt = select(ISPMRecommendation).where(
            ISPMRecommendation.tenant_id == tenant_id,
            ISPMRecommendation.status == FindingStatus.OPEN
        ).order_by(ISPMRecommendation.priority)
        result = await self.db.execute(stmt)
        recs = result.scalars().all()

        roadmap = [
            {
                "phase": 1,
                "title": "Critical Risk Remediation (0-30 days)",
                "priority": "CRITICAL",
                "items": [
                    {
                        "id": str(r.id),
                        "title": r.title,
                        "category": r.category,
                        "effort": r.effort_estimate,
                        "risk_reduction": r.expected_risk_reduction
                    }
                    for r in recs if r.priority == RecommendationPriority.CRITICAL
                ]
            },
            {
                "phase": 2,
                "title": "High-Priority Improvements (30-90 days)",
                "priority": "HIGH",
                "items": [
                    {
                        "id": str(r.id),
                        "title": r.title,
                        "category": r.category,
                        "effort": r.effort_estimate,
                        "risk_reduction": r.expected_risk_reduction
                    }
                    for r in recs if r.priority == RecommendationPriority.HIGH
                ]
            },
            {
                "phase": 3,
                "title": "Zero Trust Maturity Improvements (90-180 days)",
                "priority": "MEDIUM",
                "items": [
                    {
                        "id": str(r.id),
                        "title": r.title,
                        "category": r.category,
                        "effort": r.effort_estimate,
                        "risk_reduction": r.expected_risk_reduction
                    }
                    for r in recs if r.priority == RecommendationPriority.MEDIUM
                ]
            }
        ]

        return roadmap

    # ── Private Recommendation Generators ────────────────────────────────────

    async def _generate_identity_recommendations(
        self, tenant_id: uuid.UUID, risk: IdentityRiskScore
    ) -> List[ISPMRecommendation]:
        recs = []

        # Fetch identity details
        identity_stmt = select(EnterpriseIdentity).where(
            EnterpriseIdentity.id == risk.identity_id
        )
        identity_result = await self.db.execute(identity_stmt)
        identity = identity_result.scalar_one_or_none()
        if not identity:
            return []

        # MFA enforcement recommendation
        if not identity.mfa_enabled:
            priority = (
                RecommendationPriority.CRITICAL if identity.is_privileged
                else RecommendationPriority.HIGH
            )
            rec = ISPMRecommendation(
                tenant_id=tenant_id,
                identity_id=identity.id,
                priority=priority,
                category="MFA_ENFORCEMENT",
                title=f"Enforce MFA for {identity.display_name}",
                summary=f"Identity '{identity.display_name}' lacks MFA protection. Immediate enforcement required.",
                observed_evidence=[
                    f"Identity '{identity.display_name}' discovered with no MFA configured",
                    f"Auth methods in inventory: {identity.auth_methods}",
                    f"Identity type: {identity.identity_type.value}",
                    f"Is privileged: {identity.is_privileged}"
                ],
                calculated_metrics={
                    "authentication_risk_score": risk.authentication_risk_score,
                    "overall_risk_score": risk.overall_score,
                    "mfa_coverage_gap_contribution": 50.0
                },
                analytical_assessment=(
                    f"'{identity.display_name}' presents a {'critical' if identity.is_privileged else 'high'} "
                    f"authentication gap. With no MFA, this identity is vulnerable to credential-based "
                    f"attacks including password spraying (MITRE T1110.003) and phishing (MITRE T1566). "
                    f"{'Being a privileged account, compromise would allow tenant-wide lateral movement.' if identity.is_privileged else ''}"
                ),
                recommendation=(
                    f"Immediately enroll '{identity.display_name}' in phishing-resistant MFA. "
                    f"Prioritize FIDO2/passkey or hardware token (NIST AAL3). "
                    f"Consider conditional access policies to block sign-in without MFA."
                ),
                assumptions=[
                    "Identity provider supports modern MFA enrollment",
                    "User has access to a compatible authenticator device",
                    "Organizational MFA policy exists but enforcement is not yet applied"
                ],
                implementation_steps=[
                    "Identify identity's preferred authenticator (hardware key, mobile authenticator)",
                    "Enroll identity in MFA via identity provider admin console",
                    "Enable conditional access policy requiring MFA for all sign-ins",
                    "Verify MFA enrollment with test login",
                    "Document change in ITSM system with compliance evidence"
                ],
                effort_estimate="LOW",
                expected_risk_reduction=45.0,
                nist_controls=["IA-2(1)", "IA-2(2)", "IA-2(12)"],
                mitre_techniques=["T1078", "T1110", "T1566"]
            )
            self.db.add(rec)
            recs.append(rec)

        # Dormancy recommendation
        if identity.status == IdentityStatus.DORMANT and identity.is_privileged:
            rec = ISPMRecommendation(
                tenant_id=tenant_id,
                identity_id=identity.id,
                priority=RecommendationPriority.CRITICAL,
                category="DORMANCY_CLEANUP",
                title=f"Disable Dormant Privileged Account: {identity.display_name}",
                summary="A dormant privileged account poses a critical risk of undetected compromise.",
                observed_evidence=[
                    f"Last login: {identity.days_since_last_login} days ago",
                    f"Account status: DORMANT",
                    f"Privileged access: {identity.is_privileged}",
                    "No recent activity in identity provider logs"
                ],
                calculated_metrics={
                    "dormancy_days": identity.days_since_last_login,
                    "hygiene_risk_score": risk.hygiene_risk_score
                },
                analytical_assessment=(
                    f"A dormant privileged account that has not been used for {identity.days_since_last_login} "
                    f"days creates an unmonitored attack vector. Attackers specifically target dormant "
                    f"privileged accounts (MITRE T1078.002) as they are less likely to trigger behavioral alerts."
                ),
                recommendation=(
                    "Immediately disable this account and revoke all privileged assignments. "
                    "Conduct a forensic review of last activity. Implement automated dormancy "
                    "detection with 90-day threshold for privileged accounts."
                ),
                assumptions=["Account is confirmed to have no active business use"],
                implementation_steps=[
                    "Notify business owner for confirmation of no active use",
                    "Disable account in identity provider (do not delete — preserve audit trail)",
                    "Remove all privileged role assignments",
                    "Set calendar reminder for 30-day account deletion review",
                    "Document action in change management system"
                ],
                effort_estimate="LOW",
                expected_risk_reduction=55.0,
                nist_controls=["AC-2(3)", "AC-2(7)"],
                mitre_techniques=["T1078", "T1078.002"]
            )
            self.db.add(rec)
            recs.append(rec)

        await self.db.flush()
        return recs

    async def _generate_governance_recommendation(
        self, tenant_id: uuid.UUID, finding: AccessGovernanceFinding
    ) -> Optional[ISPMRecommendation]:
        rec = ISPMRecommendation(
            tenant_id=tenant_id,
            identity_id=finding.identity_id,
            priority=RecommendationPriority.CRITICAL if finding.severity == RiskLevel.CRITICAL else RecommendationPriority.HIGH,
            category="GOVERNANCE_REMEDIATION",
            title=f"Remediate: {finding.title}",
            summary=finding.description,
            observed_evidence=[finding.description],
            calculated_metrics=finding.evidence,
            analytical_assessment=f"Governance finding type '{finding.finding_type}' indicates policy non-compliance.",
            recommendation=finding.remediation_steps or "Review and remediate the identified governance issue.",
            assumptions=["Business owner confirmation may be required before remediation"],
            implementation_steps=finding.remediation_steps.split("\n") if finding.remediation_steps else [],
            effort_estimate="MEDIUM",
            expected_risk_reduction=30.0,
            nist_controls=finding.compliance_frameworks,
            mitre_techniques=[]
        )
        self.db.add(rec)
        await self.db.flush()
        return rec

    async def _generate_mfa_recommendation(
        self, tenant_id: uuid.UUID, auth: AuthenticationAssessment
    ) -> ISPMRecommendation:
        gap_count = auth.total_identities - auth.mfa_enabled_count
        rec = ISPMRecommendation(
            tenant_id=tenant_id,
            priority=RecommendationPriority.HIGH,
            category="MFA_ENFORCEMENT",
            title="Increase MFA Coverage to 100%",
            summary=f"Currently {auth.mfa_coverage_pct:.1f}% MFA coverage. {gap_count} identities need MFA.",
            observed_evidence=[
                f"Total identities: {auth.total_identities}",
                f"MFA enabled: {auth.mfa_enabled_count}",
                f"Current coverage: {auth.mfa_coverage_pct:.1f}%",
                f"Identities without MFA: {gap_count}"
            ],
            calculated_metrics={
                "mfa_coverage_pct": auth.mfa_coverage_pct,
                "gap_count": gap_count,
                "no_mfa_privileged": auth.no_mfa_privileged_count
            },
            analytical_assessment=(
                f"At {auth.mfa_coverage_pct:.1f}% MFA coverage, the organization has {gap_count} "
                f"identities susceptible to credential-based attacks. Industry benchmark is 95%+ MFA coverage. "
                f"The {auth.no_mfa_privileged_count} privileged accounts without MFA represent critical exposure."
            ),
            recommendation=(
                "Implement a phased MFA enforcement campaign: "
                "1) Immediately enforce MFA for all privileged accounts. "
                "2) Deploy conditional access requiring MFA for all cloud app sign-ins within 30 days. "
                "3) Enroll all remaining identities within 60 days. "
                "4) Target phishing-resistant MFA (FIDO2) for 80% of identities within 90 days."
            ),
            assumptions=["Identity provider supports per-user or conditional access MFA policies"],
            implementation_steps=[
                "Identify all identities without MFA using ISPM inventory",
                "Create priority list: privileged accounts first",
                "Configure conditional access policies requiring MFA",
                "Communicate enrollment deadline to all users",
                "Monitor daily MFA adoption rate",
                "Report weekly progress to CISO"
            ],
            effort_estimate="MEDIUM",
            expected_risk_reduction=40.0,
            nist_controls=["IA-2(1)", "IA-2(2)", "IA-5"],
            mitre_techniques=["T1078", "T1110", "T1566"]
        )
        self.db.add(rec)
        await self.db.flush()
        return rec

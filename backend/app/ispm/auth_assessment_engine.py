"""
PHOENIX X — ISPM: Authentication Assessment Engine

Evaluates tenant-wide authentication posture.
Measures MFA adoption, SSO coverage, passwordless readiness,
auth method distribution, and phishing-resistant authentication percentage.
Aligned to NIST SP 800-63B AAL2/AAL3 and NIST SP 800-207.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ispm import (
    EnterpriseIdentity, AuthenticationAssessment,
    IdentityType, IdentityStatus
)


class AuthenticationAssessmentEngine:
    """
    Tenant-wide authentication posture assessment engine.

    Measures:
    - MFA adoption rate (overall and for privileged identities)
    - SSO coverage (SAML, OIDC)
    - Passwordless/passkey readiness
    - Authentication method distribution and strength
    - Phishing-resistant authentication percentage (FIDO2, certificate-based)
    - Privileged identities without MFA (critical risk)
    - Expired/expiring certificates
    - Weak authentication exposure (password-only)

    Aligned to:
    - NIST SP 800-63B: Digital Identity Guidelines — Authentication
    - NIST SP 800-207: Zero Trust Architecture (pillar: Identity)
    - CISA Phishing-Resistant MFA Guidance
    """

    PHISHING_RESISTANT_METHODS = {"PASSKEY", "CERTIFICATE", "MFA_HARDWARE_TOKEN", "BIOMETRIC", "PASSWORDLESS"}
    STRONG_METHODS = {"PASSKEY", "CERTIFICATE", "MFA_HARDWARE_TOKEN", "BIOMETRIC", "PASSWORDLESS", "MFA_TOTP"}
    SSO_METHODS = {"SSO_SAML", "SSO_OIDC"}

    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_assessment(self, tenant_id: uuid.UUID) -> AuthenticationAssessment:
        """
        Run full authentication assessment for the tenant.
        Aggregates authentication data from all identity inventory entries.
        """
        stmt = select(EnterpriseIdentity).where(
            EnterpriseIdentity.tenant_id == tenant_id,
            EnterpriseIdentity.status != IdentityStatus.DISABLED
        )
        result = await self.db.execute(stmt)
        identities = result.scalars().all()

        total = len(identities)
        if total == 0:
            return await self._create_empty_assessment(tenant_id)

        # Core Metrics
        mfa_enabled = sum(1 for i in identities if i.mfa_enabled)
        sso_enabled = sum(
            1 for i in identities
            if any(m in self.SSO_METHODS for m in i.auth_methods)
        )
        passwordless = sum(
            1 for i in identities
            if any(m in {"PASSKEY", "PASSWORDLESS", "BIOMETRIC"} for m in i.auth_methods)
        )

        # Risk Counts
        no_mfa_privileged = sum(
            1 for i in identities if i.is_privileged and not i.mfa_enabled
        )
        password_only = sum(
            1 for i in identities
            if i.auth_methods == ["PASSWORD"] or i.auth_methods == []
        )
        weak_auth = sum(
            1 for i in identities
            if not i.mfa_enabled or (i.mfa_enabled and not any(
                m in self.STRONG_METHODS for m in i.mfa_methods
            ))
        )
        phishing_resistant = sum(
            1 for i in identities
            if any(m in self.PHISHING_RESISTANT_METHODS for m in i.auth_methods)
        )

        # Method Distribution
        auth_method_dist: Dict[str, int] = {}
        mfa_method_dist: Dict[str, int] = {}

        for identity in identities:
            for method in identity.auth_methods:
                auth_method_dist[method] = auth_method_dist.get(method, 0) + 1
            for method in identity.mfa_methods:
                mfa_method_dist[method] = mfa_method_dist.get(method, 0) + 1

        # Overall Auth Score (0-100)
        mfa_pct = mfa_enabled / total
        sso_pct = sso_enabled / total
        phishing_pct = phishing_resistant / total
        priv_mfa_pct = 1.0 - (no_mfa_privileged / max(
            sum(1 for i in identities if i.is_privileged), 1
        ))

        overall_score = (
            mfa_pct * 35 +
            sso_pct * 20 +
            phishing_pct * 30 +
            priv_mfa_pct * 15
        ) * 100

        # Upsert assessment
        existing_stmt = select(AuthenticationAssessment).where(
            AuthenticationAssessment.tenant_id == tenant_id
        )
        existing_result = await self.db.execute(existing_stmt)
        assessment = existing_result.scalar_one_or_none()

        if assessment:
            assessment.total_identities = total
            assessment.mfa_enabled_count = mfa_enabled
            assessment.mfa_coverage_pct = (mfa_enabled / total) * 100
            assessment.sso_enabled_count = sso_enabled
            assessment.sso_coverage_pct = (sso_enabled / total) * 100
            assessment.passwordless_count = passwordless
            assessment.passwordless_coverage_pct = (passwordless / total) * 100
            assessment.auth_method_distribution = auth_method_dist
            assessment.mfa_method_distribution = mfa_method_dist
            assessment.no_mfa_privileged_count = no_mfa_privileged
            assessment.weak_auth_count = weak_auth
            assessment.password_only_count = password_only
            assessment.overall_auth_score = overall_score
            assessment.phishing_resistant_pct = phishing_pct * 100
            assessment.assessed_at = datetime.now(timezone.utc)
        else:
            assessment = AuthenticationAssessment(
                tenant_id=tenant_id,
                total_identities=total,
                mfa_enabled_count=mfa_enabled,
                mfa_coverage_pct=(mfa_enabled / total) * 100,
                sso_enabled_count=sso_enabled,
                sso_coverage_pct=(sso_enabled / total) * 100,
                passwordless_count=passwordless,
                passwordless_coverage_pct=(passwordless / total) * 100,
                auth_method_distribution=auth_method_dist,
                mfa_method_distribution=mfa_method_dist,
                no_mfa_privileged_count=no_mfa_privileged,
                weak_auth_count=weak_auth,
                password_only_count=password_only,
                overall_auth_score=overall_score,
                phishing_resistant_pct=phishing_pct * 100
            )
            self.db.add(assessment)

        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment

    async def get_latest_assessment(
        self, tenant_id: uuid.UUID
    ) -> Optional[AuthenticationAssessment]:
        stmt = select(AuthenticationAssessment).where(
            AuthenticationAssessment.tenant_id == tenant_id
        ).order_by(AuthenticationAssessment.assessed_at.desc())
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _create_empty_assessment(self, tenant_id: uuid.UUID) -> AuthenticationAssessment:
        assessment = AuthenticationAssessment(tenant_id=tenant_id)
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment

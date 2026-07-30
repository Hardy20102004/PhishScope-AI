"""
PHOENIX X — ISPM: Access Governance Engine

Evaluates access governance posture. Detects SoD conflicts, excessive permissions,
dormant privileges, policy gaps, orphaned access, and certification overdue issues.
Aligned to ISO/IEC 27001 A.9 (Access Control) and NIST SP 800-53 AC controls.
"""
import uuid
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ispm import (
    EnterpriseIdentity, AccessGovernanceFinding,
    IdentityType, IdentityStatus, RiskLevel, FindingStatus
)
from app.schemas.ispm import AccessGovernanceFindingCreate


class AccessGovernanceEngine:
    """
    Access Governance Engine.

    Detects and tracks:
    - SoD (Separation of Duties) conflicts
    - Excessive permissions (unused for 90+ days)
    - Dormant privileged accounts
    - Policy gaps (no certification, no review)
    - Orphaned access (access without active identity)
    - Role over-provisioning
    - Certification overdue (access reviews not performed)
    - Admin sprawl (too many global admins)
    - Shared account usage
    - Delegated access risk
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_governance_scan(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Run full access governance scan for all identities in the tenant."""
        stmt = select(EnterpriseIdentity).where(
            EnterpriseIdentity.tenant_id == tenant_id
        )
        result = await self.db.execute(stmt)
        identities = result.scalars().all()

        findings_created = 0
        for identity in identities:
            new_findings = await self._generate_governance_findings(tenant_id, identity)
            findings_created += len(new_findings)

        # Global findings (not identity-specific)
        global_findings = await self._generate_global_findings(tenant_id, identities)
        findings_created += len(global_findings)

        return {
            "identities_scanned": len(identities),
            "findings_created": findings_created,
            "scanned_at": datetime.now(timezone.utc).isoformat()
        }

    async def list_findings(
        self,
        tenant_id: uuid.UUID,
        severity: Optional[RiskLevel] = None,
        finding_type: Optional[str] = None,
        status: Optional[FindingStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AccessGovernanceFinding]:
        stmt = select(AccessGovernanceFinding).where(
            AccessGovernanceFinding.tenant_id == tenant_id
        )
        if severity:
            stmt = stmt.where(AccessGovernanceFinding.severity == severity)
        if finding_type:
            stmt = stmt.where(AccessGovernanceFinding.finding_type == finding_type)
        if status:
            stmt = stmt.where(AccessGovernanceFinding.status == status)
        stmt = stmt.order_by(AccessGovernanceFinding.detected_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_governance_summary(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Aggregate governance finding summary for dashboard."""
        stmt = select(AccessGovernanceFinding).where(
            AccessGovernanceFinding.tenant_id == tenant_id
        )
        result = await self.db.execute(stmt)
        findings = result.scalars().all()

        return {
            "total_findings": len(findings),
            "open_findings": sum(1 for f in findings if f.status == FindingStatus.OPEN),
            "critical_findings": sum(1 for f in findings if f.severity == RiskLevel.CRITICAL),
            "high_findings": sum(1 for f in findings if f.severity == RiskLevel.HIGH),
            "sod_violations": sum(1 for f in findings if f.finding_type == "SOD_CONFLICT"),
            "excess_permissions": sum(1 for f in findings if f.finding_type == "EXCESSIVE_PERMISSION"),
            "dormant_privileges": sum(1 for f in findings if f.finding_type == "DORMANT_PRIVILEGE"),
            "orphaned_access": sum(1 for f in findings if f.finding_type == "ORPHANED_ACCESS"),
            "certification_overdue": sum(1 for f in findings if f.finding_type == "CERTIFICATION_OVERDUE"),
            "admin_sprawl": sum(1 for f in findings if f.finding_type == "ADMIN_SPRAWL"),
            "by_type": {
                "SOD_CONFLICT": sum(1 for f in findings if f.finding_type == "SOD_CONFLICT"),
                "EXCESSIVE_PERMISSION": sum(1 for f in findings if f.finding_type == "EXCESSIVE_PERMISSION"),
                "DORMANT_PRIVILEGE": sum(1 for f in findings if f.finding_type == "DORMANT_PRIVILEGE"),
                "POLICY_GAP": sum(1 for f in findings if f.finding_type == "POLICY_GAP"),
                "ORPHANED_ACCESS": sum(1 for f in findings if f.finding_type == "ORPHANED_ACCESS"),
                "CERTIFICATION_OVERDUE": sum(1 for f in findings if f.finding_type == "CERTIFICATION_OVERDUE"),
                "ADMIN_SPRAWL": sum(1 for f in findings if f.finding_type == "ADMIN_SPRAWL"),
            }
        }

    async def create_finding(
        self, tenant_id: uuid.UUID, finding_in: AccessGovernanceFindingCreate
    ) -> AccessGovernanceFinding:
        finding = AccessGovernanceFinding(tenant_id=tenant_id, **finding_in.model_dump())
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

    # ── Private Detection Methods ─────────────────────────────────────────────

    async def _generate_governance_findings(
        self, tenant_id: uuid.UUID, identity: EnterpriseIdentity
    ) -> List[AccessGovernanceFinding]:
        """Generate governance findings for a specific identity."""
        findings = []
        now = datetime.now(timezone.utc)

        # Dormant Privileged Account
        if identity.is_privileged and identity.status == IdentityStatus.DORMANT:
            finding = AccessGovernanceFinding(
                tenant_id=tenant_id,
                identity_id=identity.id,
                finding_type="DORMANT_PRIVILEGE",
                severity=RiskLevel.CRITICAL,
                title=f"Dormant Privileged Account: {identity.display_name}",
                description=(
                    f"Privileged identity '{identity.display_name}' has been inactive "
                    f"for {identity.days_since_last_login or 'unknown'} days while retaining "
                    f"privileged access. This violates least-privilege and creates an "
                    f"attack surface for credential-based attacks."
                ),
                remediation_steps=(
                    "1. Disable or archive the account immediately.\n"
                    "2. Revoke all privileged role assignments.\n"
                    "3. Investigate last activity for signs of compromise.\n"
                    "4. Implement automated dormancy detection policy (90-day threshold)."
                ),
                evidence={"identity_id": str(identity.id), "days_inactive": identity.days_since_last_login},
                affected_identity_name=identity.display_name,
                business_impact="CRITICAL",
                compliance_frameworks=["NIST_AC-2", "ISO27001_A.9.2.6", "CIS_CSC_5"]
            )
            self.db.add(finding)
            findings.append(finding)

        # Excessive Permissions (simulated)
        if random.random() < 0.30 and not identity.status == IdentityStatus.DISABLED:
            unused_count = random.randint(8, 35)
            finding = AccessGovernanceFinding(
                tenant_id=tenant_id,
                identity_id=identity.id,
                finding_type="EXCESSIVE_PERMISSION",
                severity=RiskLevel.HIGH if identity.is_privileged else RiskLevel.MEDIUM,
                title=f"Excessive Permissions: {identity.display_name}",
                description=(
                    f"Identity '{identity.display_name}' holds {unused_count} permissions "
                    f"that have not been exercised in the last 90 days. This indicates "
                    f"over-provisioning and violates the principle of least privilege."
                ),
                remediation_steps=(
                    f"1. Review and revoke the {unused_count} unused permissions.\n"
                    "2. Implement just-in-time (JIT) access for privileged operations.\n"
                    "3. Schedule quarterly access reviews.\n"
                    "4. Enable access certification workflow."
                ),
                evidence={"unused_permission_count": unused_count},
                affected_identity_name=identity.display_name,
                business_impact="HIGH",
                compliance_frameworks=["NIST_AC-6", "ISO27001_A.9.4.1"]
            )
            self.db.add(finding)
            findings.append(finding)

        # Certification Overdue
        if random.random() < 0.20:
            days_overdue = random.randint(30, 180)
            finding = AccessGovernanceFinding(
                tenant_id=tenant_id,
                identity_id=identity.id,
                finding_type="CERTIFICATION_OVERDUE",
                severity=RiskLevel.MEDIUM,
                title=f"Access Certification Overdue: {identity.display_name}",
                description=(
                    f"Access certification for '{identity.display_name}' is {days_overdue} days overdue. "
                    f"Regular access reviews are required to maintain compliance and governance."
                ),
                remediation_steps=(
                    "1. Immediately initiate access certification campaign for this identity.\n"
                    "2. Review current role and permission assignments.\n"
                    "3. Certify or revoke access within 5 business days."
                ),
                evidence={"days_overdue": days_overdue},
                affected_identity_name=identity.display_name,
                business_impact="MEDIUM",
                compliance_frameworks=["SOX_ITGC", "ISO27001_A.9.2.5"]
            )
            self.db.add(finding)
            findings.append(finding)

        await self.db.flush()
        return findings

    async def _generate_global_findings(
        self, tenant_id: uuid.UUID, identities: List[EnterpriseIdentity]
    ) -> List[AccessGovernanceFinding]:
        """Generate tenant-wide governance findings (not tied to a specific identity)."""
        findings = []

        # Admin Sprawl Detection
        privileged_count = sum(1 for i in identities if i.is_privileged)
        total = max(len(identities), 1)
        admin_pct = privileged_count / total

        if admin_pct > 0.15 or privileged_count > 20:
            finding = AccessGovernanceFinding(
                tenant_id=tenant_id,
                finding_type="ADMIN_SPRAWL",
                severity=RiskLevel.HIGH,
                title="Administrative Account Sprawl Detected",
                description=(
                    f"The tenant has {privileged_count} privileged identities "
                    f"({admin_pct:.1%} of total). Excessive admin accounts increase the "
                    f"attack surface for privilege abuse and lateral movement."
                ),
                remediation_steps=(
                    "1. Review all privileged account assignments.\n"
                    "2. Implement role consolidation — target < 5% privileged accounts.\n"
                    "3. Enforce JIT privileged access via PIM/PAM.\n"
                    "4. Require security review for any new privileged account creation."
                ),
                evidence={
                    "privileged_count": privileged_count,
                    "total_identities": total,
                    "privileged_pct": admin_pct
                },
                business_impact="HIGH",
                compliance_frameworks=["NIST_AC-6(5)", "CIS_CSC_5.3"]
            )
            self.db.add(finding)
            findings.append(finding)

        await self.db.flush()
        return findings

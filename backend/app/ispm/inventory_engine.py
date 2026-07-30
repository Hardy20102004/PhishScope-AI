"""
PHOENIX X — ISPM: Identity Inventory Engine

Manages the unified, normalized enterprise identity inventory.
Provides CRUD operations, bulk imports, search/filter, and
business metadata enrichment.
"""
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.models.ispm import (
    EnterpriseIdentity, IdentityGroup, IdentityRole,
    IdentityType, IdentityStatus, RiskLevel
)
from app.schemas.ispm import (
    EnterpriseIdentityCreate, IdentityGroupCreate, IdentityRoleCreate
)


class IdentityInventoryEngine:
    """
    Unified enterprise identity inventory management.
    Maintains a continuously synchronized, normalized catalog of all identities.

    Supports:
    - Create / upsert identities from discovery feeds
    - Search by name, email, type, provider, status
    - Bulk imports
    - Business metadata enrichment (owner, OU, department)
    - Dormancy detection
    - Summary aggregations for dashboards
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Identity CRUD ────────────────────────────────────────────────────────

    async def create_identity(
        self, tenant_id: uuid.UUID, identity_in: EnterpriseIdentityCreate
    ) -> EnterpriseIdentity:
        """Register or update an enterprise identity."""
        if identity_in.external_id:
            stmt = select(EnterpriseIdentity).where(
                EnterpriseIdentity.tenant_id == tenant_id,
                EnterpriseIdentity.source_provider == identity_in.source_provider,
                EnterpriseIdentity.external_id == identity_in.external_id
            )
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                for field, value in identity_in.model_dump(exclude_unset=True).items():
                    setattr(existing, field, value)
                await self.db.commit()
                await self.db.refresh(existing)
                return existing

        identity = EnterpriseIdentity(
            tenant_id=tenant_id,
            **identity_in.model_dump()
        )
        self.db.add(identity)
        await self.db.commit()
        await self.db.refresh(identity)
        return identity

    async def get_identity(self, identity_id: uuid.UUID) -> Optional[EnterpriseIdentity]:
        stmt = select(EnterpriseIdentity).where(EnterpriseIdentity.id == identity_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_identities(
        self,
        tenant_id: uuid.UUID,
        identity_type: Optional[IdentityType] = None,
        status: Optional[IdentityStatus] = None,
        risk_level: Optional[RiskLevel] = None,
        is_privileged: Optional[bool] = None,
        search: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[EnterpriseIdentity]:
        stmt = select(EnterpriseIdentity).where(
            EnterpriseIdentity.tenant_id == tenant_id
        )
        if identity_type:
            stmt = stmt.where(EnterpriseIdentity.identity_type == identity_type)
        if status:
            stmt = stmt.where(EnterpriseIdentity.status == status)
        if risk_level:
            stmt = stmt.where(EnterpriseIdentity.risk_level == risk_level)
        if is_privileged is not None:
            stmt = stmt.where(EnterpriseIdentity.is_privileged == is_privileged)
        if search:
            stmt = stmt.where(
                or_(
                    EnterpriseIdentity.display_name.ilike(f"%{search}%"),
                    EnterpriseIdentity.email.ilike(f"%{search}%"),
                    EnterpriseIdentity.upn.ilike(f"%{search}%"),
                    EnterpriseIdentity.department.ilike(f"%{search}%"),
                )
            )
        stmt = stmt.order_by(EnterpriseIdentity.current_risk_score.desc()).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_summary_counts(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Returns aggregated counts for the ISPM dashboard."""
        all_stmt = select(EnterpriseIdentity).where(
            EnterpriseIdentity.tenant_id == tenant_id
        )
        result = await self.db.execute(all_stmt)
        identities = result.scalars().all()

        total = len(identities)
        return {
            "total_identities": total,
            "human_identities": sum(1 for i in identities if i.identity_type == IdentityType.HUMAN),
            "service_accounts": sum(1 for i in identities if i.identity_type == IdentityType.SERVICE_ACCOUNT),
            "machine_identities": sum(1 for i in identities if i.identity_type in (
                IdentityType.MACHINE, IdentityType.MANAGED_IDENTITY, IdentityType.WORKLOAD_IDENTITY
            )),
            "privileged_identities": sum(1 for i in identities if i.is_privileged),
            "dormant_identities": sum(1 for i in identities if i.status == IdentityStatus.DORMANT),
            "orphaned_identities": sum(1 for i in identities if i.status == IdentityStatus.ORPHANED),
            "mfa_enabled_count": sum(1 for i in identities if i.mfa_enabled),
            "mfa_coverage_pct": (sum(1 for i in identities if i.mfa_enabled) / max(total, 1)) * 100,
            "critical_risk": sum(1 for i in identities if i.risk_level == RiskLevel.CRITICAL),
            "high_risk": sum(1 for i in identities if i.risk_level == RiskLevel.HIGH),
            "medium_risk": sum(1 for i in identities if i.risk_level == RiskLevel.MEDIUM),
            "low_risk": sum(1 for i in identities if i.risk_level == RiskLevel.LOW),
            "average_risk_score": (
                sum(i.current_risk_score for i in identities) / max(total, 1)
            ),
            "by_type": {
                t.value: sum(1 for i in identities if i.identity_type == t)
                for t in IdentityType
            }
        }

    # ── Group CRUD ───────────────────────────────────────────────────────────

    async def create_group(
        self, tenant_id: uuid.UUID, group_in: IdentityGroupCreate
    ) -> IdentityGroup:
        group = IdentityGroup(tenant_id=tenant_id, **group_in.model_dump())
        self.db.add(group)
        await self.db.commit()
        await self.db.refresh(group)
        return group

    async def list_groups(self, tenant_id: uuid.UUID) -> List[IdentityGroup]:
        stmt = select(IdentityGroup).where(IdentityGroup.tenant_id == tenant_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # ── Role CRUD ────────────────────────────────────────────────────────────

    async def create_role(
        self, tenant_id: uuid.UUID, role_in: IdentityRoleCreate
    ) -> IdentityRole:
        role = IdentityRole(tenant_id=tenant_id, **role_in.model_dump())
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def list_roles(self, tenant_id: uuid.UUID) -> List[IdentityRole]:
        stmt = select(IdentityRole).where(IdentityRole.tenant_id == tenant_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

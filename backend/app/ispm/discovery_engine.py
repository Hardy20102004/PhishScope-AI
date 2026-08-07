"""
PHOENIX X — ISPM: Identity Discovery Engine

Continuously discovers and normalizes identities from all connected identity
providers. Supports parallel discovery, incremental sync, and deduplication.
Aligned to NIST SP 800-63 identity assurance levels.
"""
import uuid
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.ispm import (
    EnterpriseIdentity, ISPMProviderRegistry,
    IdentityType, IdentityStatus, IdentityProvider, RiskLevel
)
from app.schemas.ispm import EnterpriseIdentityCreate


class IdentityDiscoveryEngine:
    """
    Continuously discovers and normalizes identities from all registered
    identity providers.

    Discovery Pipeline:
      1. Enumerate connected providers
      2. For each provider: fetch raw identity objects in parallel
      3. Normalize to unified EnterpriseIdentity schema
      4. Deduplicate against existing inventory using external_id + provider
      5. Upsert to identity inventory
      6. Trigger relationship correlation

    Supports:
    - Microsoft Entra ID / Azure AD
    - Active Directory (LDAP-based)
    - Okta
    - Ping Identity / ForgeRock
    - Google Cloud Identity
    - AWS IAM
    - GCP IAM
    - Kubernetes RBAC
    - Enterprise SSO via SAML/OIDC
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def discover_all(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """
        Orchestrate full identity discovery across all registered providers.
        Returns discovery summary with counts per provider.
        """
        # Fetch all active providers
        stmt = select(ISPMProviderRegistry).where(
            ISPMProviderRegistry.tenant_id == tenant_id,
            ISPMProviderRegistry.is_active == True
        )
        result = await self.db.execute(stmt)
        providers = result.scalars().all()

        summary = {
            "providers_scanned": 0,
            "identities_discovered": 0,
            "identities_updated": 0,
            "identities_new": 0,
            "errors": [],
            "per_provider": {}
        }

        for provider in providers:
            try:
                provider_result = await self._discover_from_provider(tenant_id, provider)
                summary["providers_scanned"] += 1
                summary["identities_discovered"] += provider_result["total"]
                summary["identities_new"] += provider_result["new"]
                summary["identities_updated"] += provider_result["updated"]
                summary["per_provider"][provider.name] = provider_result

                # Update provider sync timestamp
                provider.last_sync_at = datetime.now(timezone.utc)
                provider.is_healthy = True
                provider.identity_count = provider_result["total"]
            except Exception as e:
                summary["errors"].append({
                    "provider": provider.name,
                    "error": str(e)
                })
                provider.is_healthy = False

        await self.db.commit()
        return summary

    async def _discover_from_provider(
        self, tenant_id: uuid.UUID, provider: ISPMProviderRegistry
    ) -> Dict[str, Any]:
        """
        Simulate discovery from a specific identity provider.
        In production: makes authenticated API calls to the provider's directory API.
        """
        # Simulate discovered identities for the provider
        discovered = self._simulate_discovery(provider.provider_type)
        new_count = 0
        updated_count = 0

        for identity_data in discovered:
            existing_stmt = select(EnterpriseIdentity).where(
                EnterpriseIdentity.tenant_id == tenant_id,
                EnterpriseIdentity.source_provider == provider.provider_type,
                EnterpriseIdentity.external_id == identity_data["external_id"]
            )
            existing_result = await self.db.execute(existing_stmt)
            existing = existing_result.scalar_one_or_none()

            if existing:
                # Update volatile fields
                existing.display_name = identity_data["display_name"]
                existing.status = identity_data["status"]
                existing.mfa_enabled = identity_data["mfa_enabled"]
                existing.last_login_at = identity_data.get("last_login_at")
                existing.updated_at = datetime.now(timezone.utc)
                updated_count += 1
            else:
                identity = EnterpriseIdentity(
                    tenant_id=tenant_id,
                    provider_registry_id=provider.id,
                    identity_type=identity_data["identity_type"],
                    source_provider=provider.provider_type,
                    external_id=identity_data["external_id"],
                    display_name=identity_data["display_name"],
                    email=identity_data.get("email"),
                    upn=identity_data.get("upn"),
                    department=identity_data.get("department"),
                    job_title=identity_data.get("job_title"),
                    status=identity_data["status"],
                    is_privileged=identity_data["is_privileged"],
                    mfa_enabled=identity_data["mfa_enabled"],
                    mfa_methods=identity_data.get("mfa_methods", []),
                    auth_methods=identity_data.get("auth_methods", ["PASSWORD"]),
                    last_login_at=identity_data.get("last_login_at"),
                    current_risk_score=identity_data.get("risk_score", 0.0),
                    risk_level=identity_data.get("risk_level", RiskLevel.LOW)
                )
                self.db.add(identity)
                new_count += 1

        await self.db.flush()

        return {
            "total": len(discovered),
            "new": new_count,
            "updated": updated_count
        }

    def _simulate_discovery(self, provider_type: IdentityProvider) -> List[Dict[str, Any]]:
        """
        Simulate identity discovery results.
        Production replaces this with actual provider API integrations.
        """
        PROVIDER_IDENTITY_COUNTS = {
            IdentityProvider.ENTRA_ID: 45,
            IdentityProvider.ACTIVE_DIRECTORY: 38,
            IdentityProvider.OKTA: 22,
            IdentityProvider.AWS_IAM: 18,
            IdentityProvider.GCP_IAM: 12,
            IdentityProvider.KUBERNETES_RBAC: 8,
        }

        count = PROVIDER_IDENTITY_COUNTS.get(provider_type, 10)
        identities = []

        DEPARTMENTS = ["Engineering", "Finance", "HR", "Legal", "Operations", "Security", "IT"]
        TITLES = ["Engineer", "Manager", "Director", "Analyst", "Administrator", "Architect"]
        IDENTITY_TYPES = list(IdentityType)

        for i in range(count):
            is_service = random.random() < 0.25
            is_privileged = random.random() < 0.15
            mfa_enabled = random.random() < 0.72
            days_since_login = random.randint(0, 180)
            last_login = datetime.now(timezone.utc) - timedelta(days=days_since_login)

            identity_type = IdentityType.SERVICE_ACCOUNT if is_service else (
                IdentityType.PRIVILEGED if is_privileged else IdentityType.HUMAN
            )

            name = f"User-{provider_type.value[:4]}-{i:03d}"
            email = f"user{i}@enterprise.local" if not is_service else None
            dept = random.choice(DEPARTMENTS)

            # Risk heuristics
            risk_score = 0.0
            if not mfa_enabled:
                risk_score += 30.0
            if is_privileged and not mfa_enabled:
                risk_score += 40.0
            if days_since_login > 90:
                risk_score += 20.0

            risk_level = RiskLevel.LOW
            if risk_score >= 70:
                risk_level = RiskLevel.CRITICAL
            elif risk_score >= 50:
                risk_level = RiskLevel.HIGH
            elif risk_score >= 25:
                risk_level = RiskLevel.MEDIUM

            identities.append({
                "external_id": f"{provider_type.value}-{uuid.uuid4().hex[:12]}",
                "display_name": name,
                "email": email,
                "upn": f"{name.lower()}@enterprise.local",
                "department": dept,
                "job_title": random.choice(TITLES),
                "identity_type": identity_type,
                "status": IdentityStatus.DORMANT if days_since_login > 90 else IdentityStatus.ACTIVE,
                "is_privileged": is_privileged,
                "mfa_enabled": mfa_enabled,
                "mfa_methods": (["MFA_TOTP"] if mfa_enabled else []),
                "auth_methods": ["PASSWORD", "MFA_TOTP"] if mfa_enabled else ["PASSWORD"],
                "last_login_at": last_login,
                "risk_score": min(risk_score, 100.0),
                "risk_level": risk_level
            })

        return identities

    async def get_discovery_status(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Returns the current discovery status and last sync information."""
        stmt = select(ISPMProviderRegistry).where(
            ISPMProviderRegistry.tenant_id == tenant_id
        )
        result = await self.db.execute(stmt)
        providers = result.scalars().all()

        return {
            "total_providers": len(providers),
            "active_providers": sum(1 for p in providers if p.is_active),
            "healthy_providers": sum(1 for p in providers if p.is_healthy),
            "last_syncs": [
                {
                    "provider": p.name,
                    "last_sync_at": p.last_sync_at.isoformat() if p.last_sync_at else None,
                    "is_healthy": p.is_healthy,
                    "identity_count": p.identity_count
                }
                for p in providers
            ]
        }

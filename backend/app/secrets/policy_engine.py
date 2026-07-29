import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.secrets import SecretPolicy
from app.schemas.secrets import SecretPolicyCreate

class PolicyEngine:
    """
    Continuously audits the inventory against defined SecretPolicy objects.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_policy(self, tenant_id: uuid.UUID, policy_in: SecretPolicyCreate) -> SecretPolicy:
        policy = SecretPolicy(
            tenant_id=tenant_id,
            name=policy_in.name,
            description=policy_in.description,
            target_secret_type=policy_in.target_secret_type,
            max_age_days=policy_in.max_age_days,
            is_active=policy_in.is_active
        )
        self.db.add(policy)
        await self.db.commit()
        await self.db.refresh(policy)
        return policy

    async def list_policies(self, tenant_id: uuid.UUID) -> List[SecretPolicy]:
        stmt = select(SecretPolicy).where(SecretPolicy.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

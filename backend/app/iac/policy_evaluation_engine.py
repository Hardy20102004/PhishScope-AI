import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.iac import IaCPolicy
from app.schemas.iac import IaCPolicyCreate

class PolicyEvaluationEngine:
    """
    Evaluates inferred cloud architecture against IaCPolicy records.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_policy(self, tenant_id: uuid.UUID, policy_in: IaCPolicyCreate) -> IaCPolicy:
        policy = IaCPolicy(
            tenant_id=tenant_id,
            name=policy_in.name,
            description=policy_in.description,
            is_active=policy_in.is_active
        )
        self.db.add(policy)
        await self.db.commit()
        await self.db.refresh(policy)
        return policy

    async def list_policies(self, tenant_id: uuid.UUID) -> List[IaCPolicy]:
        stmt = select(IaCPolicy).where(IaCPolicy.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.governance import SecurityPolicy

class PolicyManagementEngine:
    """
    Manages the lifecycle and versioning of security policies.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_policy(self, tenant_id: uuid.UUID, name: str, domain: str, desc: str, logic: dict) -> SecurityPolicy:
        policy = SecurityPolicy(
            tenant_id=tenant_id,
            policy_name=name,
            policy_domain=domain,
            description=desc,
            rule_logic=logic,
            version=1,
            is_active=True
        )
        self.db.add(policy)
        await self.db.commit()
        await self.db.refresh(policy)
        return policy

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.pam import PAMPolicy

class PAMPolicyEngine:
    """
    Evaluates PAM policies.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_policies(self, tenant_id: uuid.UUID) -> List[PAMPolicy]:
        result = await self.db.execute(select(PAMPolicy).where(PAMPolicy.tenant_id == tenant_id))
        return result.scalars().all()

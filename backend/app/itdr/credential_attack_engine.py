import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.itdr import ITDRCredentialAttack

class CredentialAttackEngine:
    """
    Detects credential attacks like spraying and stuffing.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_attacks(self, tenant_id: uuid.UUID) -> List[ITDRCredentialAttack]:
        result = await self.db.execute(select(ITDRCredentialAttack).where(ITDRCredentialAttack.tenant_id == tenant_id))
        return result.scalars().all()

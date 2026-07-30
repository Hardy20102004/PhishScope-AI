import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.pam import PAMPrivilegedIdentity

class PrivilegeInventoryEngine:
    """
    Maintains the inventory of standing privileges.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_inventory(self, tenant_id: uuid.UUID) -> List[PAMPrivilegedIdentity]:
        result = await self.db.execute(
            select(PAMPrivilegedIdentity).where(PAMPrivilegedIdentity.tenant_id == tenant_id)
        )
        return result.scalars().all()

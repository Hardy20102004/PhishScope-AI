import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.iga import IGAAccessRequest

class AccessRequestEngine:
    """
    Handles the routing and approval workflow for access requests.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_requests(self, tenant_id: uuid.UUID) -> List[IGAAccessRequest]:
        result = await self.db.execute(select(IGAAccessRequest).where(IGAAccessRequest.tenant_id == tenant_id))
        return result.scalars().all()

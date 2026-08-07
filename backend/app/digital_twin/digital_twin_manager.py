import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.digital_twin import TwinAssetNode

class DigitalTwinManager:
    """
    Manages the virtual representation and synchronization of the enterprise environment.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_assets(self, tenant_id: uuid.UUID) -> List[TwinAssetNode]:
        result = await self.db.execute(select(TwinAssetNode).where(TwinAssetNode.tenant_id == tenant_id))
        return result.scalars().all()

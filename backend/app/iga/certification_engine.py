import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.iga import IGACertificationCampaign

class CertificationEngine:
    """
    Manages access certification campaigns (UAR).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_campaigns(self, tenant_id: uuid.UUID) -> List[IGACertificationCampaign]:
        result = await self.db.execute(select(IGACertificationCampaign).where(IGACertificationCampaign.tenant_id == tenant_id))
        return result.scalars().all()

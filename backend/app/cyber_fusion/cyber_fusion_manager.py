import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_fusion import FusionRecord

class CyberFusionManager:
    """
    The central nervous system orchestrating retrieval across SOC, DFIR, Cloud, AppSec, Identity, and Exec Intel modules.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_fusion_records(self, tenant_id: uuid.UUID) -> List[FusionRecord]:
        result = await self.db.execute(select(FusionRecord).where(FusionRecord.tenant_id == tenant_id))
        return result.scalars().all()

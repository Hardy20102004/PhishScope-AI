import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.itdr import ITDRInvestigation, InvestigationStatus

class IdentityInvestigationEngine:
    """
    Aggregates identity timelines and manages investigations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_investigations(self, tenant_id: uuid.UUID) -> List[ITDRInvestigation]:
        result = await self.db.execute(select(ITDRInvestigation).where(ITDRInvestigation.tenant_id == tenant_id))
        return result.scalars().all()
    
    async def create_investigation(self, tenant_id: uuid.UUID, data: Dict[str, Any]) -> ITDRInvestigation:
        inv = ITDRInvestigation(
            tenant_id=tenant_id,
            title=data["title"],
            description=data.get("description"),
            primary_identity=data["primary_identity"],
            status=InvestigationStatus.NEW
        )
        self.db.add(inv)
        await self.db.commit()
        await self.db.refresh(inv)
        return inv

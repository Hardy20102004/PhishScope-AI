import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.collaboration import AnalystPresence

class WorkloadManager:
    """
    Aggregates tasks across modules to calculate analyst bandwidth.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_presence(self, user_id: uuid.UUID, status: str, active_cases: int) -> AnalystPresence:
        result = await self.db.execute(select(AnalystPresence).where(AnalystPresence.user_id == user_id))
        presence = result.scalar_one_or_none()
        
        if not presence:
            presence = AnalystPresence(user_id=user_id)
            self.db.add(presence)
            
        presence.status = status
        presence.active_cases = active_cases
        
        await self.db.commit()
        await self.db.refresh(presence)
        return presence

    async def get_team_presence(self) -> list[AnalystPresence]:
        result = await self.db.execute(select(AnalystPresence))
        return result.scalars().all()

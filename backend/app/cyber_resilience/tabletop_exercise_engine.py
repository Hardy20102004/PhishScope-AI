import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_resilience import TabletopExercise

class TabletopExerciseEngine:
    """
    Manages tabletop exercise scenarios, scheduling, stakeholder assignment, and lessons learned.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_exercises(self, tenant_id: uuid.UUID) -> List[TabletopExercise]:
        result = await self.db.execute(select(TabletopExercise).where(TabletopExercise.tenant_id == tenant_id))
        return result.scalars().all()

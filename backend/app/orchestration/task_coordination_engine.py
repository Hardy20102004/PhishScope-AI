import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.orchestration import TaskAssignment

class TaskCoordinationEngine:
    """
    Manages analyst assignments, escalations, and executive briefings.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(self, tenant_id: uuid.UUID) -> List[TaskAssignment]:
        result = await self.db.execute(select(TaskAssignment).where(TaskAssignment.tenant_id == tenant_id))
        return result.scalars().all()

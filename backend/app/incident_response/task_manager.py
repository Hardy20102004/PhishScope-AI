import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.incident_response import IncidentTask

class TaskManager:
    """
    Manages investigation and containment action items tied to an incident.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, incident_id: uuid.UUID, title: str, task_type: str, user_id: uuid.UUID) -> IncidentTask:
        task = IncidentTask(
            incident_id=incident_id,
            title=title,
            task_type=task_type,
            assigned_to_id=user_id,
            status="TODO"
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task_status(self, task_id: uuid.UUID, status: str) -> IncidentTask:
        result = await self.db.execute(select(IncidentTask).where(IncidentTask.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise ValueError("Task not found")
            
        task.status = status
        await self.db.commit()
        await self.db.refresh(task)
        return task

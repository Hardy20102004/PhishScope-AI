import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.orchestration import WorkflowRecord

class WorkflowEngine:
    """
    Coordinates enterprise workflows (incidents, investigations, vulnerability reviews, identity governance).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_workflows(self, tenant_id: uuid.UUID) -> List[WorkflowRecord]:
        result = await self.db.execute(select(WorkflowRecord).where(WorkflowRecord.tenant_id == tenant_id))
        return result.scalars().all()

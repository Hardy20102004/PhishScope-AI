import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.orchestration import PlaybookDefinition

class PlaybookEngine:
    """
    Manages the execution, versioning, and exception handling of defensive playbooks.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_playbooks(self, tenant_id: uuid.UUID) -> List[PlaybookDefinition]:
        result = await self.db.execute(select(PlaybookDefinition).where(PlaybookDefinition.tenant_id == tenant_id))
        return result.scalars().all()

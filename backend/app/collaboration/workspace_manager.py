import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.collaboration import CollabWorkspace

class WorkspaceManager:
    """
    Manages the creation and access control of shared team collaboration rooms.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workspace(self, name: str, workspace_type: str, tenant_id: uuid.UUID, entity_id: uuid.UUID = None) -> CollabWorkspace:
        workspace = CollabWorkspace(
            tenant_id=tenant_id,
            name=name,
            workspace_type=workspace_type,
            linked_entity_id=entity_id
        )
        self.db.add(workspace)
        await self.db.commit()
        await self.db.refresh(workspace)
        return workspace

    async def get_workspace(self, workspace_id: uuid.UUID) -> CollabWorkspace:
        result = await self.db.execute(select(CollabWorkspace).where(CollabWorkspace.id == workspace_id))
        return result.scalar_one_or_none()

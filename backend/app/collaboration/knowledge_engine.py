import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.collaboration import AnalystNote

class KnowledgeEngine:
    """
    Manages the creation and indexing of shared markdown notes and playbooks.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_note(self, title: str, content: str, author_id: uuid.UUID, workspace_id: uuid.UUID = None) -> AnalystNote:
        note = AnalystNote(
            title=title,
            content=content,
            author_id=author_id,
            workspace_id=workspace_id
        )
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def get_workspace_notes(self, workspace_id: uuid.UUID) -> list[AnalystNote]:
        result = await self.db.execute(
            select(AnalystNote)
            .where(AnalystNote.workspace_id == workspace_id)
            .order_by(AnalystNote.updated_at.desc())
        )
        return result.scalars().all()

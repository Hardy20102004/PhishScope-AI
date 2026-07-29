import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.collaboration import ChatMessage

class MessagingService:
    """
    Handles sending, threading, and retrieving secure chat messages within a Workspace.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post_message(self, workspace_id: uuid.UUID, sender_id: uuid.UUID, content: str, is_system: bool = False) -> ChatMessage:
        message = ChatMessage(
            workspace_id=workspace_id,
            sender_id=sender_id,
            content=content,
            is_system_message=is_system
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages(self, workspace_id: uuid.UUID, limit: int = 50) -> list[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.workspace_id == workspace_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
        )
        return result.scalars().all()

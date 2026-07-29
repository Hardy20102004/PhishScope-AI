import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.soc_copilot import CopilotSession, CopilotChatMessage
from app.soc_copilot.reasoning_engine import ReasoningEngine

class ConversationEngine:
    """
    Manages multi-turn AI interactions and orchestrates prompt processing.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.reasoning = ReasoningEngine(db)

    async def create_session(self, title: str, context_tags: list, tenant_id: uuid.UUID, user_id: uuid.UUID) -> CopilotSession:
        session = CopilotSession(
            tenant_id=tenant_id,
            user_id=user_id,
            title=title,
            context_tags=context_tags
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def send_message(self, session_id: uuid.UUID, content: str) -> CopilotChatMessage:
        # 1. Log User Message
        user_msg = CopilotChatMessage(session_id=session_id, role="USER", content=content)
        self.db.add(user_msg)
        
        # 2. Trigger Reasoning & Retrieval
        ai_response, citations, log = await self.reasoning.process_prompt(session_id, content)
        
        # 3. Log AI Response
        ai_msg = CopilotChatMessage(
            session_id=session_id, 
            role="ASSISTANT", 
            content=ai_response,
            evidence_citations=citations
        )
        self.db.add(ai_msg)
        
        # 4. Attach Reasoning Log to AI Message
        log.message_id = ai_msg.id
        self.db.add(log)
        
        await self.db.commit()
        await self.db.refresh(ai_msg)
        return ai_msg

    async def get_session(self, session_id: uuid.UUID) -> CopilotSession:
        result = await self.db.execute(select(CopilotSession).where(CopilotSession.id == session_id))
        return result.scalar_one_or_none()

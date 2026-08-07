import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.copilot import CopilotConversation, CopilotMessage, MessageRole
from app.models.investigation import Investigation
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.llm_service import MockLLMService
from app.services.ai.prompt_manager import PromptManager


class ConversationManager:
    """Manages chat history and coordinates LLM responses."""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = MockLLMService() # Using mock for now
        
    async def chat(self, investigation_id: uuid.UUID, message_content: str) -> CopilotMessage:
        """Processes a new user message and returns the AI's response."""
        
        # 1. Fetch Investigation Context
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        investigation = self.db.execute(stmt).scalar_one_or_none()
        if not investigation:
            raise ValueError("Investigation not found")
            
        context = ContextBuilder.build_investigation_context(investigation)
        
        # 2. Get or Create Conversation
        stmt = select(CopilotConversation).where(CopilotConversation.investigation_id == investigation_id)
        conversation = self.db.execute(stmt).scalar_one_or_none()
        
        if not conversation:
            conversation = CopilotConversation(investigation_id=investigation_id)
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            
        # 3. Store User Message
        user_message = CopilotMessage(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=message_content
        )
        self.db.add(user_message)
        self.db.commit()
        
        # 4. Build message history for LLM
        # Fetch last 10 messages for context window
        stmt = select(CopilotMessage).where(CopilotMessage.conversation_id == conversation.id).order_by(CopilotMessage.created_at.desc()).limit(10)
        recent_messages = self.db.execute(stmt).scalars().all()
        recent_messages.reverse() # chronological order
        
        formatted_messages = [
            {"role": msg.role.value.lower(), "content": msg.content}
            for msg in recent_messages
        ]
        
        # 5. Generate Response
        ai_response_text = await self.llm_service.generate_response(
            system_prompt=PromptManager.COPILOT_SYSTEM_PROMPT,
            messages=formatted_messages,
            context=context
        )
        
        # 6. Store AI Response
        ai_message = CopilotMessage(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=ai_response_text,
            evidence_references=[] # Mock doesn't generate structured citations yet
        )
        self.db.add(ai_message)
        self.db.commit()
        self.db.refresh(ai_message)
        
        return ai_message
        
    def get_history(self, investigation_id: uuid.UUID) -> List[CopilotMessage]:
        stmt = select(CopilotConversation).where(CopilotConversation.investigation_id == investigation_id)
        conversation = self.db.execute(stmt).scalar_one_or_none()
        
        if not conversation:
            return []
            
        return conversation.messages

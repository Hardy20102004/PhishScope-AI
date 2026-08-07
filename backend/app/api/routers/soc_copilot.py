import uuid
from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.soc_copilot import (
    CopilotSessionCreate,
    CopilotSessionResponse,
    CopilotChatMessageCreate,
    CopilotChatMessageResponse
)

from app.soc_copilot.conversation_engine import ConversationEngine

router = APIRouter()

@router.post("/sessions", response_model=CopilotSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_copilot_session(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    session_in: CopilotSessionCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Instantiate a new AI SOC Copilot conversation session.
    """
    engine = ConversationEngine(db)
    return await engine.create_session(
        title=session_in.title,
        context_tags=session_in.context_tags,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id
    )

@router.post("/sessions/{session_id}/chat", response_model=CopilotChatMessageResponse)
async def chat(
    session_id: uuid.UUID,
    msg_in: CopilotChatMessageCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Send a message to the AI Copilot and trigger the Reasoning/Evidence engines.
    """
    engine = ConversationEngine(db)
    return await engine.send_message(
        session_id=session_id,
        content=msg_in.content
    )

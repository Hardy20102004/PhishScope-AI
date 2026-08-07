import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models.user import User
from app.models.collaboration import CollabWorkspace, ChatMessage, AnalystNote, AnalystPresence
from app.schemas.collaboration import (
    CollabWorkspaceCreate, CollabWorkspaceResponse,
    ChatMessageCreate, ChatMessageResponse,
    AnalystNoteCreate, AnalystNoteResponse,
    AnalystPresenceResponse
)

from app.collaboration.workspace_manager import WorkspaceManager
from app.collaboration.messaging_service import MessagingService
from app.collaboration.knowledge_engine import KnowledgeEngine
from app.collaboration.workload_manager import WorkloadManager
from app.collaboration.ai_collab_assistant import AICollabAssistant

router = APIRouter()

@router.post("/workspaces", response_model=CollabWorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    workspace_in: CollabWorkspaceCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new shared Workspace Room.
    """
    manager = WorkspaceManager(db)
    workspace = await manager.create_workspace(
        name=workspace_in.name,
        workspace_type=workspace_in.workspace_type,
        tenant_id=current_user.tenant_id,
        entity_id=workspace_in.linked_entity_id
    )
    return workspace

@router.post("/workspaces/{workspace_id}/messages", response_model=ChatMessageResponse)
async def post_message(
    workspace_id: uuid.UUID,
    msg_in: ChatMessageCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    manager = MessagingService(db)
    msg = await manager.post_message(
        workspace_id=workspace_id,
        sender_id=current_user.id,
        content=msg_in.content,
        is_system=msg_in.is_system_message
    )
    return msg

@router.get("/workspaces/{workspace_id}/messages", response_model=List[ChatMessageResponse])
async def get_messages(
    workspace_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    manager = MessagingService(db)
    return await manager.get_messages(workspace_id=workspace_id)

@router.post("/notes", response_model=AnalystNoteResponse)
async def create_note(
    note_in: AnalystNoteCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    manager = KnowledgeEngine(db)
    note = await manager.create_note(
        title=note_in.title,
        content=note_in.content,
        author_id=current_user.id,
        workspace_id=note_in.workspace_id
    )
    return note

@router.get("/team/presence", response_model=List[AnalystPresenceResponse])
async def get_team_presence(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    manager = WorkloadManager(db)
    return await manager.get_team_presence()

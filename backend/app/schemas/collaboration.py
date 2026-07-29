import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Chat Message
class ChatMessageBase(BaseModel):
    content: str
    is_system_message: bool = False

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    sender_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Analyst Note
class AnalystNoteBase(BaseModel):
    title: str
    content: str

class AnalystNoteCreate(AnalystNoteBase):
    workspace_id: Optional[uuid.UUID] = None

class AnalystNoteResponse(AnalystNoteBase):
    id: uuid.UUID
    author_id: uuid.UUID
    workspace_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Workspace
class CollabWorkspaceBase(BaseModel):
    name: str
    workspace_type: str
    linked_entity_id: Optional[uuid.UUID] = None

class CollabWorkspaceCreate(CollabWorkspaceBase):
    pass

class CollabWorkspaceResponse(CollabWorkspaceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    # Optional relationships loaded on demand
    messages: List[ChatMessageResponse] = []
    notes: List[AnalystNoteResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Analyst Presence
class AnalystPresenceResponse(BaseModel):
    user_id: uuid.UUID
    status: str
    active_cases: int
    last_active: datetime
    
    model_config = ConfigDict(from_attributes=True)

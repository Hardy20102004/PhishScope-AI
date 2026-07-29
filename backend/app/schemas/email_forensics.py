import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Headers
class EmailHeaderBase(BaseModel):
    header_name: str
    header_value: str
    hop_index: Optional[int]
    parsed_data: Optional[Dict[str, Any]]

class EmailHeaderResponse(EmailHeaderBase):
    id: uuid.UUID
    message_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Messages
class EmailMessageBase(BaseModel):
    message_id_header: Optional[str]
    subject: Optional[str]
    sender: str
    recipients: str
    body_text: Optional[str]
    is_phishing_suspect: bool
    auth_pass: bool
    timestamp: datetime

class EmailMessageResponse(EmailMessageBase):
    id: uuid.UUID
    mailbox_id: uuid.UUID
    headers: List[EmailHeaderResponse] = []
    model_config = ConfigDict(from_attributes=True)

# Mailboxes
class MailboxBase(BaseModel):
    name: str
    source_type: str
    owner_email: Optional[str]

class MailboxCreate(MailboxBase):
    investigation_id: Optional[uuid.UUID] = None

class MailboxResponse(MailboxBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    uploaded_at: datetime
    
    messages: List[EmailMessageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

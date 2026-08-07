from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.email_forensics import (
    MailboxCreate,
    MailboxResponse
)

from app.email_forensics.mailbox_manager import MailboxManager
from app.email_forensics.message_parser import MessageParser
from app.email_forensics.auth_engine import AuthEngine
from app.email_forensics.routing_engine import RoutingEngine

router = APIRouter()

@router.post("/mailboxes", response_model=MailboxResponse, status_code=status.HTTP_201_CREATED)
async def upload_mailbox(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    mailbox_in: MailboxCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Registers a new mailbox/EML and parses messages, routing headers, and authentication blocks.
    """
    # 1. Register Mailbox
    mgr = MailboxManager(db)
    mailbox = await mgr.register_mailbox(
        tenant_id=current_user.tenant_id,
        name=mailbox_in.name,
        source_type=mailbox_in.source_type,
        owner_email=mailbox_in.owner_email,
        inv_id=mailbox_in.investigation_id
    )
    
    # 2. Extract Messages
    msg_engine = MessageParser(db)
    messages = await msg_engine.parse_messages(mailbox.id)
    
    # 3. Analyze Headers for each message
    auth_engine = AuthEngine(db)
    routing_engine = RoutingEngine(db)
    
    for msg in messages:
        await auth_engine.analyze_auth(msg.id, msg.is_phishing_suspect)
        await routing_engine.analyze_routing(msg.id, msg.is_phishing_suspect)
        
    await db.refresh(mailbox, ["messages"])
    # Note: normally we'd do a deeper query to load headers for each message, but for the MVP mock this suffices.
    return mailbox

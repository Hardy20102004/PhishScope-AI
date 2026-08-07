import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email_forensics import Mailbox

class MailboxManager:
    """
    Handles ingestion of email containers (PST, EML, MBOX).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_mailbox(self, tenant_id: uuid.UUID, name: str, source_type: str, owner_email: str = None, inv_id: uuid.UUID = None) -> Mailbox:
        mailbox = Mailbox(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            name=name,
            source_type=source_type,
            owner_email=owner_email
        )
        
        self.db.add(mailbox)
        await self.db.commit()
        await self.db.refresh(mailbox)
        return mailbox

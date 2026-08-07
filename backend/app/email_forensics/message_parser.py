import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email_forensics import EmailMessage

class MessageParser:
    """
    Simulates parsing an EML/MSG file to extract the body, sender, and recipients.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def parse_messages(self, mailbox_id: uuid.UUID) -> list[EmailMessage]:
        now = datetime.now(timezone.utc)
        
        # Mocking extracted email messages
        messages = [
            EmailMessage(
                mailbox_id=mailbox_id,
                message_id_header="<20260727.xyz@phish.net>",
                subject="URGENT: Password Expiry Notification",
                sender="admin@microsoft-secure-update.com",
                recipients="jdoe@company.com",
                body_text="Dear user,\n\nYour password expires in 24 hours. Please click here to retain access: http://login-microsoft-secure.com/auth\n\nIT Support",
                is_phishing_suspect=True,
                auth_pass=False, # We will simulate this failing DKIM/SPF
                timestamp=now - timedelta(days=1, hours=2)
            ),
            EmailMessage(
                mailbox_id=mailbox_id,
                message_id_header="<20260727.abc@company.com>",
                subject="Re: Project Update",
                sender="boss@company.com",
                recipients="jdoe@company.com",
                body_text="Thanks for the update. Let's discuss tomorrow.",
                is_phishing_suspect=False,
                auth_pass=True,
                timestamp=now - timedelta(days=1, hours=1)
            )
        ]
        
        for msg in messages:
            self.db.add(msg)
            
        await self.db.commit()
        return messages

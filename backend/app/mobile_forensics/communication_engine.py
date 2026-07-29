import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.mobile_forensics import ForensicMobileCommunication

class CommunicationEngine:
    """
    Simulates extracting messaging SQLite databases (sms.db, ChatStorage.sqlite) and reconstructing threaded conversations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def extract_messages(self, device_id: uuid.UUID) -> list[ForensicMobileCommunication]:
        now = datetime.now(timezone.utc)
        
        # Mocking an extracted SMS thread
        messages = [
            ForensicMobileCommunication(
                device_id=device_id,
                app_name="iMessage",
                thread_id="THREAD_001",
                sender="+15551234567", # Target Device
                receiver="+15559998888", # Suspect
                body="Did you delete the server logs?",
                is_outgoing=True,
                is_deleted=False,
                timestamp=now - timedelta(days=1, hours=2)
            ),
            ForensicMobileCommunication(
                device_id=device_id,
                app_name="iMessage",
                thread_id="THREAD_001",
                sender="+15559998888",
                receiver="+15551234567",
                body="Yeah, wiped everything and cleared the bash history.",
                is_outgoing=False,
                is_deleted=True, # Found in sqlite unallocated space
                timestamp=now - timedelta(days=1, hours=1, minutes=55)
            )
        ]
        
        for msg in messages:
            self.db.add(msg)
            
        await self.db.commit()
        return messages

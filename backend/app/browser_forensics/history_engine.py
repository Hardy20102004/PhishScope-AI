import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.browser_forensics import BrowserHistory

class HistoryEngine:
    """
    Simulates parsing History SQLite databases and crossing referencing with Threat Intel.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def extract_history(self, profile_id: uuid.UUID) -> list[BrowserHistory]:
        now = datetime.now(timezone.utc)
        
        # Mocking extracted browser history
        history_records = [
            BrowserHistory(
                profile_id=profile_id,
                url="https://mail.google.com/mail/u/0/#inbox",
                title="Inbox - Google Workspace",
                visit_count=42,
                is_threat_hit=False,
                timestamp=now - timedelta(days=1, hours=2)
            ),
            BrowserHistory(
                profile_id=profile_id,
                url="http://login-microsoft-secure.com/auth",
                title="Microsoft Account Login",
                visit_count=1,
                is_threat_hit=True, # Flagged by Threat Intel
                threat_category="Credential Phishing",
                timestamp=now - timedelta(days=1, hours=1, minutes=55)
            )
        ]
        
        for record in history_records:
            self.db.add(record)
            
        await self.db.commit()
        return history_records

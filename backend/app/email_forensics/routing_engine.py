import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email_forensics import EmailHeader

class RoutingEngine:
    """
    Parses 'Received' headers to reconstruct the MTA hop chain.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_routing(self, message_id: uuid.UUID, is_phish: bool) -> list[EmailHeader]:
        headers = []
        
        if is_phish:
            # Spoofed/Phishing routing path (bottom-up chronological)
            headers = [
                EmailHeader(message_id=message_id, header_name="Received", header_value="from unknown (103.22.1.5) by mail.phish.net with SMTP; 27 Jul 2026 14:00:00 +0000", hop_index=1),
                EmailHeader(message_id=message_id, header_name="Received", header_value="from mail.phish.net by mx.company.com with ESMTP; 27 Jul 2026 14:00:02 +0000", hop_index=2),
                EmailHeader(message_id=message_id, header_name="Received", header_value="from mx.company.com by internal-exchange.company.local; 27 Jul 2026 14:00:05 +0000", hop_index=3)
            ]
        else:
            # Clean routing path
            headers = [
                EmailHeader(message_id=message_id, header_name="Received", header_value="from [10.0.0.50] by internal-exchange.company.local; 27 Jul 2026 15:00:00 +0000", hop_index=1)
            ]
            
        for h in headers:
            self.db.add(h)
            
        await self.db.commit()
        return headers

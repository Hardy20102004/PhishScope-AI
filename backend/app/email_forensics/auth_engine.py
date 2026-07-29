import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.email_forensics import EmailHeader

class AuthEngine:
    """
    Analyzes Authentication-Results headers for SPF, DKIM, and DMARC alignment.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_auth(self, message_id: uuid.UUID, is_phish: bool) -> EmailHeader:
        # Simulate generating the Authentication-Results header
        
        if is_phish:
            raw_val = "spf=fail (sender IP is 103.22.1.5) smtp.mailfrom=microsoft-secure-update.com; dkim=fail (body hash did not verify); dmarc=fail action=quarantine"
            parsed = {"spf": "fail", "dkim": "fail", "dmarc": "fail", "reason": "IP not authorized, hash mismatch"}
        else:
            raw_val = "spf=pass (sender IP is 10.0.0.1) smtp.mailfrom=company.com; dkim=pass (signature verified); dmarc=pass action=none"
            parsed = {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
            
        header = EmailHeader(
            message_id=message_id,
            header_name="Authentication-Results",
            header_value=raw_val,
            parsed_data=parsed
        )
        
        self.db.add(header)
        await self.db.commit()
        return header

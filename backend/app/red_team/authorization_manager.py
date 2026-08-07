import uuid
import hashlib
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.red_team import AuthorizationRecord, RedTeamCampaign

class AuthorizationManager:
    """
    Manages stakeholder approvals and digital signature generation for campaigns.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sign_authorization(self, record_id: uuid.UUID, stakeholder_id: str) -> AuthorizationRecord:
        result = await self.db.execute(select(AuthorizationRecord).where(AuthorizationRecord.id == record_id))
        record = result.scalar_one_or_none()
        
        if not record:
            raise ValueError("Authorization Record not found")
            
        # Ensure the campaign is in the correct state
        camp_res = await self.db.execute(select(RedTeamCampaign).where(RedTeamCampaign.id == record.campaign_id))
        campaign = camp_res.scalar_one_or_none()
        if campaign.status != "PENDING_APPROVAL":
            raise ValueError("Campaign is not currently accepting approvals.")
            
        # Generate simulated cryptographic signature tying the approval to the scope and time
        sig_payload = f"{record.id}:{campaign.id}:{stakeholder_id}:{datetime.now(timezone.utc).isoformat()}"
        signature = hashlib.sha256(sig_payload.encode('utf-8')).hexdigest()
        
        record.is_approved = True
        record.approved_at = datetime.now(timezone.utc)
        record.signature_hash = signature
        record.stakeholder_id = stakeholder_id
        
        await self.db.commit()
        await self.db.refresh(record)
        
        # Check if this was the last signature needed
        all_res = await self.db.execute(select(AuthorizationRecord).where(AuthorizationRecord.campaign_id == campaign.id))
        all_records = all_res.scalars().all()
        if all([a.is_approved for a in all_records]):
            campaign.status = "AUTHORIZED"
            await self.db.commit()
            
        return record

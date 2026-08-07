import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.red_team import RedTeamCampaign, AuthorizationRecord

class CampaignManager:
    """
    Orchestrates the Red Team Campaign lifecycle and enforces strict governance gates.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_campaign(self, tenant_id: uuid.UUID, name: str, description: str, scope: dict) -> RedTeamCampaign:
        campaign = RedTeamCampaign(
            tenant_id=tenant_id,
            name=name,
            description=description,
            scope_definition=scope,
            status="DRAFT"
        )
        self.db.add(campaign)
        await self.db.flush()
        
        # Scaffold required approvals (e.g. Legal, CISO, App Owner)
        roles = ["CISO", "LEGAL_COUNSEL", "SYSTEM_OWNER"]
        for role in roles:
            auth = AuthorizationRecord(
                campaign_id=campaign.id,
                stakeholder_role=role,
                stakeholder_id=f"pending_{role.lower()}@company.com"
            )
            self.db.add(auth)
            
        await self.db.commit()
        await self.db.refresh(campaign, ["approvals"])
        return campaign

    async def request_authorization(self, campaign_id: uuid.UUID) -> RedTeamCampaign:
        result = await self.db.execute(select(RedTeamCampaign).where(RedTeamCampaign.id == campaign_id))
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise ValueError("Campaign not found")
            
        if campaign.status != "DRAFT":
            raise ValueError("Only DRAFT campaigns can be submitted for approval")
            
        campaign.status = "PENDING_APPROVAL"
        await self.db.commit()
        return campaign

    async def commence_campaign(self, campaign_id: uuid.UUID) -> RedTeamCampaign:
        result = await self.db.execute(select(RedTeamCampaign).where(RedTeamCampaign.id == campaign_id))
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise ValueError("Campaign not found")
            
        # Enforcement Gate: Ensure all stakeholders have approved
        res = await self.db.execute(select(AuthorizationRecord).where(AuthorizationRecord.campaign_id == campaign.id))
        approvals = res.scalars().all()
        
        if not all([a.is_approved for a in approvals]):
            raise PermissionError("Cannot commence campaign. Not all required authorizations have been digitally signed.")
            
        campaign.status = "IN_PROGRESS"
        campaign.start_date = datetime.now(timezone.utc)
        await self.db.commit()
        return campaign

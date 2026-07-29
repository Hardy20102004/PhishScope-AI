import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.red_team import CampaignFinding, RedTeamCampaign
from sqlalchemy import select

class FindingsManager:
    """
    Tracks vulnerabilities and detection gaps identified during the campaign.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_finding(self, campaign_id: uuid.UUID, title: str, description: str, severity: str, tactic: str, technique_id: str) -> CampaignFinding:
        # Ensure campaign is active
        camp_res = await self.db.execute(select(RedTeamCampaign).where(RedTeamCampaign.id == campaign_id))
        campaign = camp_res.scalar_one_or_none()
        
        if not campaign or campaign.status != "IN_PROGRESS":
            raise PermissionError("Findings can only be logged for IN_PROGRESS campaigns.")
            
        finding = CampaignFinding(
            campaign_id=campaign_id,
            title=title,
            description=description,
            severity=severity,
            tactic=tactic,
            technique_id=technique_id
        )
        
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

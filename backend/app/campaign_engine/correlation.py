from sqlalchemy.orm import Session
from app.campaign_engine.models import Campaign, CampaignInfrastructure, CampaignVictim
import uuid

class CampaignCorrelationEngine:
    """
    Handles linking specific infrastructure or victimology to an existing Campaign cluster.
    """
    def __init__(self, db: Session):
        self.db = db

    def link_infrastructure(self, campaign_id: uuid.UUID, indicator_id: uuid.UUID, usage: str = None) -> CampaignInfrastructure:
        link = CampaignInfrastructure(
            campaign_id=campaign_id,
            indicator_id=indicator_id,
            usage=usage
        )
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link

    def link_victim(self, campaign_id: uuid.UUID, sector: str, region: str) -> CampaignVictim:
        victim = CampaignVictim(
            campaign_id=campaign_id,
            sector=sector,
            region=region
        )
        self.db.add(victim)
        self.db.commit()
        self.db.refresh(victim)
        return victim

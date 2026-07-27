from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional

from app.campaign_engine.models import Campaign
from app.knowledge_graph.managers import EntityManager

class CampaignKGSync:
    """
    Synchronizes Campaign clusters to the Enterprise Knowledge Graph.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.entity_manager = EntityManager(db)

    def sync_campaign(self, campaign: Campaign) -> Optional[object]:
        """
        Creates or updates a Campaign node in the Knowledge Graph.
        """
        try:
            properties = {
                "campaign_id": str(campaign.id),
                "description": campaign.description,
                "status": campaign.status,
                "severity": campaign.severity
            }
                
            tenant_id_str = str(campaign.tenant_id) if campaign.tenant_id else None

            return self.entity_manager.create_entity(
                entity_type="CAMPAIGN",
                name=campaign.name,
                tenant_id=tenant_id_str,
                properties=properties,
                confidence=campaign.confidence
            )
        except Exception as e:
            logger.error(f"Failed to sync Campaign to KG: {e}")
            return None

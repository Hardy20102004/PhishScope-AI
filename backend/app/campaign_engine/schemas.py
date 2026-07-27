from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field
import uuid
from datetime import datetime

from app.campaign_engine.models import CampaignStatus, CampaignSeverity

class CampaignInfrastructureBase(BaseModel):
    indicator_id: uuid.UUID
    usage: Optional[str] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None

class CampaignVictimBase(BaseModel):
    sector: Optional[str] = None
    region: Optional[str] = None
    organization_name: Optional[str] = None
    targeted_at: Optional[datetime] = None

class CampaignTimelineBase(BaseModel):
    event_time: datetime
    event_type: str
    description: str

class CampaignEvidenceBase(BaseModel):
    evidence_type: str
    description: str
    confidence: float

class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    aliases: Optional[List[str]] = None
    status: CampaignStatus = CampaignStatus.EMERGING
    severity: CampaignSeverity = CampaignSeverity.MEDIUM
    confidence: float = 0.0
    first_observed: Optional[datetime] = None
    last_observed: Optional[datetime] = None

class CampaignCreate(CampaignBase):
    pass

class CampaignResponse(CampaignBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    infrastructure_count: int = 0
    victim_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class CampaignDiscoveryResponse(BaseModel):
    message: str
    clusters_found: int
    new_campaigns_created: int

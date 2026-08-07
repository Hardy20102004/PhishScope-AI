from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger

from app.api import deps
from app.campaign_engine.schemas import (
    CampaignCreate,
    CampaignResponse,
    CampaignDiscoveryResponse,
    CampaignTimelineBase
)
from app.campaign_engine.models import Campaign, CampaignTimeline
from app.campaign_engine.discovery import CampaignClusteringEngine
from app.campaign_engine.timeline import CampaignTimelineEngine

router = APIRouter()

@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    *,
    db: Session = Depends(deps.get_db),
    campaign_in: CampaignCreate,
) -> Any:
    """
    Manually create a new Campaign profile.
    """
    campaign = Campaign(**campaign_in.model_dump())
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    List all campaigns.
    """
    return db.query(Campaign).offset(skip).limit(limit).all()

@router.post("/discover", response_model=CampaignDiscoveryResponse)
def trigger_campaign_discovery(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Trigger the AI-powered Campaign Clustering Engine to find emerging campaigns.
    """
    engine = CampaignClusteringEngine(db)
    clusters, new_campaigns = engine.discover_campaigns()
    
    return {
        "message": "Discovery scan completed.",
        "clusters_found": clusters,
        "new_campaigns_created": new_campaigns
    }

@router.get("/{campaign_id}/timeline", response_model=List[CampaignTimelineBase])
def get_campaign_timeline(
    campaign_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get the chronological evolution of a campaign.
    """
    engine = CampaignTimelineEngine(db)
    return engine.get_timeline(campaign_id)

@router.get("/analytics/summary")
def get_campaign_analytics(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get high-level analytics for the Campaign Dashboard.
    """
    total_campaigns = db.query(Campaign).count()
    active = db.query(Campaign).filter(Campaign.status == "Active").count()
    emerging = db.query(Campaign).filter(Campaign.status == "Emerging").count()
    
    return {
        "total_campaigns": total_campaigns,
        "active_campaigns": active,
        "emerging_clusters": emerging,
        "infrastructure_reuse_rate": 0.42, # Mock metric
        "regional_trends": {"North America": 60, "Europe": 30, "Asia": 10}
    }

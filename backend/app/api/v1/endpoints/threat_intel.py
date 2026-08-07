from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.threat_intel import IndicatorResponse, IndicatorSearchRequest
from app.services.threat_intel.manager import ThreatIntelManager

router = APIRouter()

@router.get("/indicators/{value:path}", response_model=IndicatorResponse)
async def get_indicator(
    value: str,
    force_refresh: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get threat intelligence for a specific indicator.
    Accepts URLs, IP addresses, domains, hashes, and email addresses.
    """
    manager = ThreatIntelManager(db)
    indicator = await manager.get_indicator(value, force_refresh)
    
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
        
    return indicator

@router.post("/indicators/search", response_model=IndicatorResponse)
async def search_indicator(
    request: IndicatorSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Search for an indicator via POST to avoid URL encoding issues with complex URLs.
    """
    manager = ThreatIntelManager(db)
    indicator = await manager.get_indicator(request.value)
    
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
        
    return indicator

@router.get("/feeds/status")
async def get_feeds_status(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the health status of all threat intelligence connectors.
    """
    # Mocking status for now since manager doesn't expose it directly yet
    return {
        "status": "ok",
        "connectors": [
            {"name": "virustotal", "status": "healthy"},
            {"name": "google_safe_browsing", "status": "healthy"}
        ]
    }

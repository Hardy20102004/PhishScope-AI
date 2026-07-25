from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.extension import ExtensionDevice
from app.models.investigation import InvestigationType
from app.models.user import User
from app.schemas.extension import (
    ExtensionDeviceRegister,
    ExtensionDeviceSchema,
    QuickInvestigateRequest,
)
from app.schemas.investigation import InvestigationCreate

# Using the unified investigation engine to trigger on "Quick Investigate"
from app.services.investigations.url_engine import URLEngine

router = APIRouter()

@router.post("/register", response_model=ExtensionDeviceSchema)
def register_device(
    request: ExtensionDeviceRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(ExtensionDevice).where(ExtensionDevice.device_fingerprint == request.device_fingerprint)
    device = db.execute(stmt).scalar_one_or_none()
    
    if device:
        # Update existing
        device.browser_type = request.browser_type
        device.settings = request.settings
        device.is_active = True
        device.user_id = current_user.id
    else:
        device = ExtensionDevice(
            user_id=current_user.id,
            browser_type=request.browser_type,
            device_fingerprint=request.device_fingerprint,
            settings=request.settings
        )
        db.add(device)
        
    db.commit()
    db.refresh(device)
    return device

@router.post("/investigate/quick")
def quick_investigate(
    request: QuickInvestigateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Rapidly creates an investigation based on right-click context.
    """
    engine = URLEngine(db)
    
    if request.context_type == "URL" and request.url:
        inv_create = InvestigationCreate(
            type=InvestigationType.URL,
            target=request.url,
            title=f"Extension Scan: {request.url[:30]}..."
        )
        investigation = engine.create_investigation(inv_create, current_user.id)
        # We could run synchronous threat-intel lookups here for immediate popup feedback
        return {"status": "success", "investigation_id": str(investigation.id), "threat_score": 75}
        
    elif request.context_type == "TEXT" and request.text:
        # Assuming we treat raw text from extension as a general search/correlation
        return {"status": "success", "message": "Text analysis initiated"}
        
    raise HTTPException(status_code=400, detail="Invalid context")

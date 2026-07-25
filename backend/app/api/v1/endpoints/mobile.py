from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.mobile import MobileDevice
from app.models.user import User
from app.schemas.mobile import MobileDeviceSchema, MobileEnrollmentRequest, SyncRequest

router = APIRouter()

@router.post("/enroll", response_model=MobileDeviceSchema)
def enroll_device(
    request: MobileEnrollmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(MobileDevice).where(MobileDevice.device_id == request.device_id)
    device = db.execute(stmt).scalar_one_or_none()
    
    if device:
        device.platform = request.platform
        device.os_version = request.os_version
        device.is_biometric_enabled = request.is_biometric_enabled
        device.push_token = request.push_token
        device.user_id = current_user.id
    else:
        device = MobileDevice(
            user_id=current_user.id,
            device_id=request.device_id,
            platform=request.platform,
            os_version=request.os_version,
            is_biometric_enabled=request.is_biometric_enabled,
            push_token=request.push_token
        )
        db.add(device)
        
    db.commit()
    db.refresh(device)
    return device

@router.put("/sync")
def sync_offline_data(
    request: SyncRequest,
    device_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(MobileDevice).where(MobileDevice.device_id == device_id, MobileDevice.user_id == current_user.id)
    device = db.execute(stmt).scalar_one_or_none()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not enrolled")
        
    if not device.is_compliant:
        raise HTTPException(status_code=403, detail="Device is not compliant with MDM policies")

    # In a real app, we would process request.offline_queue here
    # e.g., syncing new cases, uploading evidence offline, etc.
    processed_count = len(request.offline_queue)
    
    device.last_sync_at = datetime.now(timezone.utc)
    db.commit()
    
    return {
        "status": "success", 
        "processed_items": processed_count,
        "server_time": datetime.now(timezone.utc)
    }

@router.post("/push-token")
def update_push_token(
    device_id: str,
    token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(MobileDevice).where(MobileDevice.device_id == device_id, MobileDevice.user_id == current_user.id)
    device = db.execute(stmt).scalar_one_or_none()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not enrolled")
        
    device.push_token = token
    db.commit()
    
    return {"status": "success"}

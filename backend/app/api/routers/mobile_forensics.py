from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.mobile_forensics import (
    MobileDeviceCreate,
    MobileDeviceResponse
)

from app.mobile_forensics.device_manager import DeviceManager
from app.mobile_forensics.communication_engine import CommunicationEngine
from app.mobile_forensics.location_engine import LocationEngine

router = APIRouter()

@router.post("/devices", response_model=MobileDeviceResponse, status_code=status.HTTP_201_CREATED)
async def upload_mobile_acquisition(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    device_in: MobileDeviceCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Registers a new mobile acquisition (backup/dump) and extracts messaging and location artifacts.
    """
    # 1. Register Device
    mgr = DeviceManager(db)
    device = await mgr.register_device(
        tenant_id=current_user.tenant_id,
        name=device_in.device_name,
        os_type=device_in.os_type,
        os_version=device_in.os_version,
        acq_type=device_in.acquisition_type,
        imei=device_in.imei,
        inv_id=device_in.investigation_id
    )
    
    # 2. Extract Communications
    comm_engine = CommunicationEngine(db)
    await comm_engine.extract_messages(device.id)
    
    # 3. Extract Locations
    loc_engine = LocationEngine(db)
    await loc_engine.extract_locations(device.id)
        
    await db.refresh(device, ["communications", "locations"])
    return device

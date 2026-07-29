import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.mobile_forensics import MobileDevice

class DeviceManager:
    """
    Handles ingestion of mobile backups or logical acquisitions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_device(self, tenant_id: uuid.UUID, name: str, os_type: str, os_version: str, acq_type: str, imei: str = None, inv_id: uuid.UUID = None) -> MobileDevice:
        device = MobileDevice(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            device_name=name,
            os_type=os_type,
            os_version=os_version,
            acquisition_type=acq_type,
            imei=imei
        )
        
        self.db.add(device)
        await self.db.commit()
        await self.db.refresh(device)
        return device

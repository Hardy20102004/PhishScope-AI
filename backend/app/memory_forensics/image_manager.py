import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.memory_forensics import MemoryImage

class ImageManager:
    """
    Handles ingestion of volatile memory dumps and sets the OS profile.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_image(self, tenant_id: uuid.UUID, filename: str, os_profile: str, size: int, inv_id: uuid.UUID = None) -> MemoryImage:
        image = MemoryImage(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            filename=filename,
            os_profile=os_profile,
            size_bytes=size
        )
        
        self.db.add(image)
        await self.db.commit()
        await self.db.refresh(image)
        return image

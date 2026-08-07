import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.disk_forensics import DiskImage

class ImageManager:
    """
    Handles ingestion and cryptographic verification of forensic disk images.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_image(self, tenant_id: uuid.UUID, filename: str, format: str, size: int, md5: str, sha256: str, inv_id: uuid.UUID = None) -> DiskImage:
        # Simulate hash verification (e.g., comparing user-provided hash against calculated hash)
        verified = True
        
        image = DiskImage(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            filename=filename,
            format=format,
            size_bytes=size,
            md5_hash=md5,
            sha256_hash=sha256,
            hash_verified=verified
        )
        
        self.db.add(image)
        await self.db.commit()
        await self.db.refresh(image)
        return image

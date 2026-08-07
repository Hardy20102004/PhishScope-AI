from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.disk_forensics import (
    DiskImageCreate,
    DiskImageResponse
)

from app.disk_forensics.image_manager import ImageManager
from app.disk_forensics.fs_analysis_engine import FileSystemAnalysisEngine
from app.disk_forensics.recovery_engine import RecoveryEngine

router = APIRouter()

@router.post("/images", response_model=DiskImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_disk_image(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    image_in: DiskImageCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Registers a new forensic disk image, parses its file system, and recovers deleted files.
    """
    # 1. Register and Hash Verify
    mgr = ImageManager(db)
    image = await mgr.register_image(
        tenant_id=current_user.tenant_id,
        filename=image_in.filename,
        format=image_in.format,
        size=image_in.size_bytes,
        md5=image_in.md5_hash,
        sha256=image_in.sha256_hash,
        inv_id=image_in.investigation_id
    )
    
    # 2. Parse File System Tree
    fs_engine = FileSystemAnalysisEngine(db)
    partitions = await fs_engine.parse_image(image.id)
    
    # 3. Carve Unallocated Space
    recovery_engine = RecoveryEngine(db)
    for partition in partitions:
        await recovery_engine.carve_unallocated_space(partition.id)
        
    await db.refresh(image, ["partitions"])
    return image

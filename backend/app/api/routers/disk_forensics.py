from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.disk_forensics import DiskImage, DiskPartition, ForensicArtifact
from app.schemas.disk_forensics import (
    DiskImageCreate,
    DiskImageResponse
)

from app.disk_forensics.image_manager import ImageManager
from app.disk_forensics.fs_analysis_engine import FileSystemAnalysisEngine
from app.disk_forensics.recovery_engine import RecoveryEngine
from app.disk_forensics.timeline_builder import TimelineBuilder

router = APIRouter()

@router.get("/images", response_model=List[DiskImageResponse])
async def list_disk_images(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List all forensic disk images registered for the user's tenant.
    """
    stmt = select(DiskImage).where(DiskImage.tenant_id == current_user.tenant_id)
    result = await db.execute(stmt)
    images = result.scalars().all()
    return images

@router.get("/images/{image_id}", response_model=DiskImageResponse)
async def get_disk_image(
    image_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get detailed information about a specific disk image.
    """
    stmt = select(DiskImage).where(DiskImage.id == image_id, DiskImage.tenant_id == current_user.tenant_id)
    result = await db.execute(stmt)
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Disk image not found")
    return image

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

@router.post("/images/{image_id}/parse", response_model=DiskImageResponse)
async def parse_disk_image(
    image_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Triggers parsing and carving for an image.
    """
    stmt = select(DiskImage).where(DiskImage.id == image_id, DiskImage.tenant_id == current_user.tenant_id)
    result = await db.execute(stmt)
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Disk image not found")

    fs_engine = FileSystemAnalysisEngine(db)
    partitions = await fs_engine.parse_image(image.id)
    
    recovery_engine = RecoveryEngine(db)
    for partition in partitions:
        await recovery_engine.carve_unallocated_space(partition.id)

    image.hash_verified = True
    await db.commit()
    await db.refresh(image, ["partitions"])
    return image

@router.get("/artifacts")
async def list_artifacts(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List extracted forensic artifacts across all tenant images.
    """
    stmt = select(ForensicArtifact)
    result = await db.execute(stmt)
    artifacts = result.scalars().all()
    return artifacts

@router.get("/timeline")
async def get_timeline(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get synthesized MAC timeline events.
    """
    builder = TimelineBuilder()
    return builder.generate_timeline()


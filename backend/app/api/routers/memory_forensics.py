from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.memory_forensics import (
    MemoryImageCreate,
    MemoryImageResponse
)

from app.memory_forensics.image_manager import ImageManager
from app.memory_forensics.process_engine import ProcessEngine
from app.memory_forensics.network_engine import NetworkEngine

router = APIRouter()

@router.post("/dumps", response_model=MemoryImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_memory_dump(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    image_in: MemoryImageCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Registers a new memory dump, detects the OS profile, and parses processes/networks.
    """
    # 1. Register
    mgr = ImageManager(db)
    image = await mgr.register_image(
        tenant_id=current_user.tenant_id,
        filename=image_in.filename,
        os_profile=image_in.os_profile,
        size=image_in.size_bytes,
        inv_id=image_in.investigation_id
    )
    
    # 2. Extract Processes
    process_engine = ProcessEngine(db)
    await process_engine.extract_processes(image.id)
    
    # 3. Extract Networks
    network_engine = NetworkEngine(db)
    await network_engine.extract_connections(image.id)
        
    await db.refresh(image, ["processes", "network_connections"])
    return image

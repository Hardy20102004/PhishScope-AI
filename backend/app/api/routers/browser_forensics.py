from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.browser_forensics import (
    BrowserProfileCreate,
    BrowserProfileResponse
)

from app.browser_forensics.profile_manager import ProfileManager
from app.browser_forensics.history_engine import HistoryEngine
from app.browser_forensics.extension_engine import ExtensionEngine

router = APIRouter()

@router.post("/profiles", response_model=BrowserProfileResponse, status_code=status.HTTP_201_CREATED)
async def upload_browser_profile(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    profile_in: BrowserProfileCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Registers a new browser profile extraction and parses history/extensions.
    """
    # 1. Register Profile
    mgr = ProfileManager(db)
    profile = await mgr.register_profile(
        tenant_id=current_user.tenant_id,
        browser_type=profile_in.browser_type,
        profile_name=profile_in.profile_name,
        host_os=profile_in.host_os,
        inv_id=profile_in.investigation_id
    )
    
    # 2. Extract History
    hist_engine = HistoryEngine(db)
    await hist_engine.extract_history(profile.id)
    
    # 3. Extract Extensions
    ext_engine = ExtensionEngine(db)
    await ext_engine.extract_extensions(profile.id)
        
    await db.refresh(profile, ["history_records", "extensions"])
    return profile

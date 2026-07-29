from typing import Any
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.api import deps
from app.models.user import User
from app.schemas.blue_team import (
    ReadinessSnapshotResponse
)

from app.blue_team.readiness_manager import ReadinessManager

router = APIRouter()

@router.get("/readiness", response_model=ReadinessSnapshotResponse)
async def get_blue_team_readiness(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Calculates and retrieves the current Operational Maturity Score for the Blue Team.
    """
    mgr = ReadinessManager(db)
    snapshot = await mgr.get_current_readiness(current_user.tenant_id)
    return snapshot

from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.unified_timeline import (
    UnifiedInvestigationCreate,
    UnifiedInvestigationResponse
)

from app.unified_timeline.timeline_manager import TimelineManager
from app.unified_timeline.correlation_engine import CorrelationEngine
from app.unified_timeline.relationship_engine import RelationshipEngine

router = APIRouter()

@router.post("/sessions", response_model=UnifiedInvestigationResponse, status_code=status.HTTP_201_CREATED)
async def generate_unified_timeline(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    inv_in: UnifiedInvestigationCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Creates a new unified timeline session, imports raw events from disparate modules, and runs correlation.
    """
    # 1. Create Session
    mgr = TimelineManager(db)
    session = await mgr.create_unified_session(
        tenant_id=current_user.tenant_id,
        name=inv_in.name,
        inv_id=inv_in.investigation_id
    )
    
    # 2. Import Module Events (Disk, Memory, Cloud, Email)
    events = await mgr.import_mock_events(session.id)
    
    # 3. Correlate by Shared IOCs (e.g. IP Address)
    corr_eng = CorrelationEngine(db)
    await corr_eng.correlate_events(session.id, events)
    
    # 4. Infer Causal Relationships (e.g. Email receipt -> Payload Drop)
    rel_eng = RelationshipEngine(db)
    await rel_eng.infer_causality(session.id, events)
        
    await db.refresh(session, ["events", "correlations"])
    return session

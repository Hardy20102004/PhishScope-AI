import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models.user import User
from app.models.threat_hunting import HuntSession, HuntQuery, HuntHypothesis
from app.schemas.threat_hunting import (
    HuntSessionCreate, HuntSessionResponse, HuntQueryCreate, HuntQueryResponse, HuntHypothesisResponse
)

from app.threat_hunting.hunt_manager import ThreatHuntManager

router = APIRouter()

@router.post("/sessions", response_model=HuntSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_hunt_session(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    session_in: HuntSessionCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new Threat Hunt session.
    """
    manager = ThreatHuntManager(db)
    session = await manager.create_session(
        title=session_in.title,
        objective=session_in.objective,
        user_id=current_user.id,
        tenant_id=current_user.tenant_id
    )
    return session

@router.get("/sessions", response_model=List[HuntSessionResponse])
async def list_hunt_sessions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List active threat hunt sessions.
    """
    result = await db.execute(
        select(HuntSession)
        .where(HuntSession.tenant_id == current_user.tenant_id)
        .order_by(HuntSession.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/sessions/{session_id}/query", response_model=HuntQueryResponse)
async def execute_hunt_query(
    session_id: uuid.UUID,
    query_in: HuntQueryCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Execute a natural language query within a hunt session.
    """
    manager = ThreatHuntManager(db)
    query_record = await manager.execute_query(session_id, query_in.raw_query)
    return query_record

@router.post("/sessions/{session_id}/hypothesize", response_model=List[HuntHypothesisResponse])
async def generate_hypotheses(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate AI-backed hypotheses for the current hunt session based on gathered queries and evidence.
    """
    manager = ThreatHuntManager(db)
    hypotheses = await manager.generate_hypotheses_for_session(session_id)
    return hypotheses

import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models.user import User
from app.models.incident_response import Incident, DFIRCase, EvidenceRecord
from app.schemas.incident_response import (
    IncidentCreate, IncidentResponse, IncidentUpdate,
    EvidenceRecordCreate, EvidenceRecordResponse
)
from app.incident_response.incident_manager import IncidentManager
from app.incident_response.evidence_manager import EvidenceManager

router = APIRouter()

@router.post("/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    incident_in: IncidentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new Incident and auto-provision the default DFIR Case.
    """
    manager = IncidentManager(db)
    incident = await manager.create_incident(
        title=incident_in.title,
        description=incident_in.description,
        severity=incident_in.severity,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id
    )
    
    # Reload with relationships
    result = await db.execute(
        select(Incident)
        .options(selectinload(Incident.cases), selectinload(Incident.tasks))
        .where(Incident.id == incident.id)
    )
    return result.scalar_one()

@router.get("/incidents", response_model=List[IncidentResponse])
async def list_incidents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List open incidents for the SOC Dashboard.
    """
    result = await db.execute(
        select(Incident)
        .options(selectinload(Incident.cases), selectinload(Incident.tasks))
        .where(Incident.tenant_id == current_user.tenant_id)
        .order_by(Incident.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/cases/{case_id}/evidence", response_model=EvidenceRecordResponse)
async def attach_evidence(
    case_id: uuid.UUID,
    evidence_in: EvidenceRecordCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Attach evidence to a case, automatically generating the immutable Chain of Custody log.
    """
    manager = EvidenceManager(db)
    evidence = await manager.attach_evidence(
        case_id=case_id,
        artifact_type=evidence_in.artifact_type,
        artifact_value=evidence_in.artifact_value,
        source=evidence_in.source,
        user_id=current_user.id
    )
    
    result = await db.execute(
        select(EvidenceRecord)
        .options(selectinload(EvidenceRecord.chain_of_custody))
        .where(EvidenceRecord.id == evidence.id)
    )
    return result.scalar_one()

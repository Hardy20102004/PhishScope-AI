from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from uuid import UUID
from datetime import datetime, timezone

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.investigation import Investigation, InvestigationStatus
from app.schemas.investigation import InvestigationCreate, InvestigationResponse
from app.schemas.base import APIResponse
from app.api.responses import success_response, error_response
from app.services.investigations.url_engine import URLEngine

router = APIRouter()

@router.post("/", response_model=APIResponse[InvestigationResponse])
def create_investigation(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    investigation_in: InvestigationCreate
) -> Any:
    """Submit a new artifact for investigation."""
    
    # 1. Initialize the DB record
    db_obj = Investigation(
        target=investigation_in.target,
        type=investigation_in.type,
        status=InvestigationStatus.PROCESSING,
        user_id=current_user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # 2. Run the Engine Synchronously (Phase 10/11 approach)
    if investigation_in.type == "URL":
        from app.services.investigations.url_engine import URLEngine
        engine = URLEngine(target=investigation_in.target)
        success = engine.run_pipeline()
    elif investigation_in.type == "WEBSITE":
        from app.services.investigations.website_engine import WebsiteEngine
        engine = WebsiteEngine(target=investigation_in.target)
        success = engine.run_pipeline()
    elif investigation_in.type == "EMAIL":
        from app.services.investigations.email_engine import EmailEngine
        engine = EmailEngine(target=investigation_in.target, raw_content=investigation_in.raw_content)
        success = engine.run_pipeline()
    elif investigation_in.type == "MESSAGING":
        from app.services.investigations.messaging_engine import MessagingEngine
        engine = MessagingEngine(target=investigation_in.target, raw_content=investigation_in.raw_content)
        success = engine.run_pipeline()
    elif investigation_in.type == "QR":
        from app.services.investigations.qr_engine import QREngine
        engine = QREngine(target=investigation_in.target, raw_content=investigation_in.raw_content)
        success = engine.run_pipeline()
    else:
        # Other types not yet implemented
        db_obj.status = InvestigationStatus.FAILED
        db_obj.error_message = f"{investigation_in.type} engine not implemented yet."
        db_obj.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_obj)
        return success_response(db_obj)

    if success:
        db_obj.status = InvestigationStatus.COMPLETED
        db_obj.risk_score = engine.risk_score
        db_obj.risk_level = engine.risk_level
        db_obj.evidence = engine.evidence
        db_obj.findings = [f.model_dump() for f in engine.findings]
    else:
        db_obj.status = InvestigationStatus.FAILED
        db_obj.error_message = engine.error_message
        
    db_obj.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_obj)
        
    return success_response(db_obj)

@router.get("/", response_model=APIResponse[List[InvestigationResponse]])
def read_investigations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Retrieve investigations created by the current user."""
    # Descending order by created_at
    investigations = db.query(Investigation).filter(
        Investigation.user_id == current_user.id
    ).order_by(Investigation.created_at.desc()).offset(skip).limit(limit).all()
    
    return success_response(investigations)

@router.get("/{id}", response_model=APIResponse[InvestigationResponse])
def read_investigation(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get a specific investigation by ID."""
    investigation = db.query(Investigation).filter(
        Investigation.id == id,
        Investigation.user_id == current_user.id
    ).first()
    
    if not investigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investigation not found"
        )
        
    return success_response(investigation)

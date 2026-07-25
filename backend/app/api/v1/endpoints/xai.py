from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.xai import ExplanationResponse
from app.xai.manager import ExplanationManager
from app.models.xai import ExplanationRecord
from app.models.decision import DecisionRecord

router = APIRouter()

@router.post("/generate/{decision_id}", response_model=ExplanationResponse)
def generate_explanation(decision_id: str, db: Session = Depends(deps.get_db)):
    """Triggers the XAI pipeline for a specific decision."""
    manager = ExplanationManager(db)
    try:
        return manager.generate_explanation(decision_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{decision_id}", response_model=ExplanationResponse)
def get_explanation(decision_id: str, db: Session = Depends(deps.get_db)):
    """Fetches an existing explanation for a decision."""
    # Try to fetch existing
    explanation = db.query(ExplanationRecord).filter_by(decision_id=decision_id).first()
    
    if not explanation:
        # Check if decision exists
        decision = db.query(DecisionRecord).filter_by(id=decision_id).first()
        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")
        # Generate on the fly if requested and not found but decision exists
        manager = ExplanationManager(db)
        return manager.generate_explanation(decision_id)
        
    return explanation

@router.get("/", response_model=List[ExplanationResponse])
def list_explanations(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return db.query(ExplanationRecord).order_by(ExplanationRecord.created_at.desc()).offset(skip).limit(limit).all()

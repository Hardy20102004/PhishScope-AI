from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.decision import DecisionCreate, DecisionResponse, HumanReviewRequest
from app.decision.manager import DecisionManager
from app.decision.human_review import HumanReviewService
from app.models.decision import DecisionRecord

router = APIRouter()

@router.post("/evaluate", response_model=DecisionResponse)
def evaluate_decision(req: DecisionCreate, db: Session = Depends(deps.get_db)):
    """Submit context/evidence for the AI Engine to evaluate and propose a decision."""
    manager = DecisionManager(db)
    return manager.evaluate(req)

@router.get("/", response_model=List[DecisionResponse])
def list_decisions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return db.query(DecisionRecord).order_by(DecisionRecord.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{decision_id}", response_model=DecisionResponse)
def get_decision(decision_id: str, db: Session = Depends(deps.get_db)):
    decision = db.query(DecisionRecord).filter_by(id=decision_id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

@router.post("/{decision_id}/review", response_model=DecisionResponse)
def review_decision(
    decision_id: str, 
    req: HumanReviewRequest, 
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    """Human oversight endpoint to Approve or Reject a decision."""
    service = HumanReviewService(db)
    try:
        return service.review_decision(
            decision_id=decision_id,
            user_id=current_user.id,
            action=req.action,
            comments=req.comments
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

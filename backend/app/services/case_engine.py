from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, update
import uuid
from typing import List

from app.models.case_management import Case, DecisionLog
from app.models.investigation import Investigation
from app.schemas.case_management import CaseCreate, CaseUpdate, DecisionLogCreate
from app.services.timeline_engine import TimelineEngine

class CaseEngine:
    def __init__(self, db: Session):
        self.db = db
        self.timeline = TimelineEngine(db)
        
    def create_case(self, case_data: CaseCreate, user_id: uuid.UUID) -> Case:
        new_case = Case(
            title=case_data.title,
            description=case_data.description,
            priority=case_data.priority,
            tags=case_data.tags,
            owner_id=user_id
        )
        self.db.add(new_case)
        self.db.commit()
        self.db.refresh(new_case)
        
        self.timeline.add_event(
            case_id=new_case.id,
            action="CASE_CREATED",
            details="Case was initialized.",
            user_id=user_id
        )
        
        return new_case
        
    def get_case(self, case_id: uuid.UUID) -> Case:
        stmt = select(Case).options(
            selectinload(Case.tasks),
            selectinload(Case.timeline_events),
            selectinload(Case.investigations),
            selectinload(Case.decisions)
        ).where(Case.id == case_id)
        case = self.db.execute(stmt).scalar_one_or_none()
        if not case:
            raise ValueError("Case not found")
        return case
        
    def list_cases(self) -> List[Case]:
        stmt = select(Case).order_by(Case.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())
        
    def update_case(self, case_id: uuid.UUID, case_data: CaseUpdate, user_id: uuid.UUID) -> Case:
        case = self.get_case(case_id)
        
        updated_fields = []
        if case_data.title is not None and case.title != case_data.title:
            case.title = case_data.title
            updated_fields.append("title")
        if case_data.status is not None and case.status != case_data.status:
            case.status = case_data.status
            updated_fields.append("status")
        if case_data.priority is not None and case.priority != case_data.priority:
            case.priority = case_data.priority
            updated_fields.append("priority")
            
        self.db.commit()
        self.db.refresh(case)
        
        if updated_fields:
            self.timeline.add_event(
                case_id=case.id,
                action="CASE_UPDATED",
                details=f"Updated fields: {', '.join(updated_fields)}",
                user_id=user_id
            )
            
        return case
        
    def link_investigation(self, case_id: uuid.UUID, investigation_id: uuid.UUID, user_id: uuid.UUID):
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        investigation = self.db.execute(stmt).scalar_one_or_none()
        if not investigation:
            raise ValueError("Investigation not found")
            
        investigation.case_id = case_id
        self.db.commit()
        
        self.timeline.add_event(
            case_id=case_id,
            action="INVESTIGATION_LINKED",
            details=f"Linked investigation {investigation_id}",
            metadata={"investigation_id": str(investigation_id)},
            user_id=user_id
        )
        
    def record_decision(self, case_id: uuid.UUID, decision_data: DecisionLogCreate, user_id: uuid.UUID) -> DecisionLog:
        decision = DecisionLog(
            case_id=case_id,
            user_id=user_id,
            decision=decision_data.decision,
            reasoning=decision_data.reasoning,
            confidence_score=decision_data.confidence_score,
            evidence_references=decision_data.evidence_references
        )
        self.db.add(decision)
        self.db.commit()
        self.db.refresh(decision)
        
        self.timeline.add_event(
            case_id=case_id,
            action="DECISION_RECORDED",
            details=f"Decision: {decision.decision}",
            metadata={"decision_id": str(decision.id)},
            user_id=user_id
        )
        
        return decision

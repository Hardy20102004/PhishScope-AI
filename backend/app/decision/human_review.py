import structlog
from sqlalchemy.orm import Session
from app.models.decision import DecisionRecord, DecisionState, ApprovalWorkflow

logger = structlog.get_logger("phoenix.decision.human_review")

class HumanReviewService:
    def __init__(self, db: Session):
        self.db = db
        
    def review_decision(self, decision_id: str, user_id: str, action: str, comments: str = None) -> DecisionRecord:
        decision = self.db.query(DecisionRecord).filter_by(id=decision_id).first()
        if not decision:
            raise ValueError("Decision not found")
            
        if decision.state not in [DecisionState.PENDING_REVIEW, DecisionState.POLICY_BLOCKED]:
            raise ValueError(f"Decision is not pending review. Current state: {decision.state}")
            
        new_state = None
        if action == "APPROVE":
            new_state = DecisionState.APPROVED
        elif action == "REJECT":
            new_state = DecisionState.REJECTED
        else:
            raise ValueError("Invalid action")
            
        decision.state = new_state
        
        workflow_log = ApprovalWorkflow(
            decision_id=decision.id,
            user_id=user_id,
            action=action,
            comments=comments
        )
        self.db.add(workflow_log)
        self.db.commit()
        self.db.refresh(decision)
        
        logger.info("decision_reviewed", decision_id=decision.id, action=action)
        return decision

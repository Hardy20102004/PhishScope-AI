from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai_brain.governance import AIAuditEngine
from app.api import deps
from app.models.multi_agent import AgentDefinition, ApprovalStatus, HumanApprovalRequest
from app.multi_agent.manager import AgentManager
from app.schemas.multi_agent import (
    AgentDefinitionResponse,
    HumanApprovalResponse,
    HumanApprovalSubmit,
    PlanRequest,
    PlanResponse,
)

router = APIRouter()

@router.get("/agents", response_model=List[AgentDefinitionResponse])
async def get_active_agents(db: Session = Depends(deps.get_db)):
    """List all specialized agents in the enterprise workforce."""
    agents = db.query(AgentDefinition).all()
    return agents

@router.post("/agents/initialize")
async def initialize_default_agents(db: Session = Depends(deps.get_db)):
    """Seed the database with the default multi-agent workforce."""
    audit_engine = AIAuditEngine()
    manager = AgentManager(db=db, core_audit_engine=audit_engine)
    manager.initialize_workforce()
    return {"status": "Workforce Initialized"}

@router.post("/plan", response_model=PlanResponse)
async def generate_workflow_plan(request: PlanRequest, db: Session = Depends(deps.get_db)):
    """Decompose an investigative objective into an executable DAG of agent tasks."""
    # Placeholder for planner
    return PlanResponse(plan_id="plan-123", tasks=[], estimated_duration_seconds=0, agents_involved=[])

@router.post("/execute/{plan_id}")
async def execute_workflow(plan_id: str, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    """Initiates asynchronous DAG execution using the ExecutionEngine."""
    return {"status": "Execution Started", "plan_id": plan_id}

@router.get("/approvals", response_model=List[HumanApprovalResponse])
async def list_pending_approvals(db: Session = Depends(deps.get_db)):
    """Fetch all tasks blocked by Human-in-the-Loop gating."""
    approvals = db.query(HumanApprovalRequest).filter(HumanApprovalRequest.status == ApprovalStatus.PENDING).all()
    return approvals

@router.post("/approvals/{request_id}/decision")
async def submit_human_decision(request_id: str, decision: HumanApprovalSubmit, db: Session = Depends(deps.get_db)):
    """Submit an analyst approval or override to resume paused workflows."""
    approval = db.query(HumanApprovalRequest).filter(HumanApprovalRequest.id == request_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    approval.status = decision.status
    approval.reviewer_user_id = decision.reviewer_user_id
    approval.reviewer_feedback = decision.reviewer_feedback
    db.commit()
    return {"status": "Resolved", "request_id": request_id}

@router.get("/stream/{plan_id}")
async def stream_workflow_progress(plan_id: str):
    """Server-Sent Events (SSE) endpoint streaming live agent tasks and messaging bus logs."""
    # Would return EventSourceResponse generator in production
    return {"message": "Streaming endpoint (SSE placeholder)"}

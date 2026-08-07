import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

import structlog

from app.models.multi_agent import ApprovalStatus, MessageType
from app.multi_agent.communication import CommunicationBus
from app.schemas.multi_agent import HumanApprovalResponse

logger = structlog.get_logger("phoenix.multi_agent.human")

class HumanInTheLoopEngine:
    """
    Manages workflow gating, requiring human analyst authorization for high-risk actions
    or low-confidence/conflicted agent conclusions.
    """
    def __init__(self, comm_bus: CommunicationBus):
        self.comm_bus = comm_bus
        self._pending_approvals: Dict[str, HumanApprovalResponse] = {}

    def request_approval(self, task_id: str, agent_id: str, description: str, severity: str = "MODERATE") -> HumanApprovalResponse:
        """
        Pauses an agent workflow and generates a Human Approval Request.
        """
        request_id = str(uuid.uuid4())
        
        req = HumanApprovalResponse(
            id=request_id,
            task_id=task_id,
            requesting_agent_id=agent_id,
            description=description,
            risk_severity=severity,
            status=ApprovalStatus.PENDING,
            created_at=datetime.now(timezone.utc)
        )
        
        self._pending_approvals[request_id] = req
        logger.info("human_approval_requested", request_id=request_id, task_id=task_id, agent=agent_id)
        
        # Broadcast the request so the frontend UI can pick it up via SSE
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(
                self.comm_bus.publish(
                    sender_id="system-hitl",
                    message_type=MessageType.EVENT,
                    content={"event": "APPROVAL_REQUIRED", "request": req.model_dump(mode="json")},
                    correlation_id=task_id
                )
            )
        
        return req

    def submit_decision(self, request_id: str, reviewer_id: str, status: ApprovalStatus, feedback: Optional[str] = None) -> HumanApprovalResponse:
        """
        Processes an analyst's decision (Approve/Reject/Override) and resumes the workflow.
        """
        if request_id not in self._pending_approvals:
            raise ValueError(f"Approval request {request_id} not found or already processed.")
            
        req = self._pending_approvals[request_id]
        req.status = status
        req.reviewer_user_id = uuid.UUID(reviewer_id) if isinstance(reviewer_id, str) else reviewer_id
        req.reviewer_feedback = feedback
        req.resolved_at = datetime.now(timezone.utc)
        
        logger.info("human_approval_resolved", request_id=request_id, status=status.value)
        
        # In a fully asynchronous workflow engine, resolving this request would trigger
        # an Event that resumes the paused asyncio task.
        
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(
                self.comm_bus.publish(
                    sender_id="system-hitl",
                    message_type=MessageType.EVENT,
                    content={"event": "APPROVAL_RESOLVED", "request": req.model_dump(mode="json")},
                    correlation_id=str(req.task_id)
                )
            )
        
        del self._pending_approvals[request_id]
        return req

    def get_pending_approvals(self) -> List[HumanApprovalResponse]:
        return list(self._pending_approvals.values())

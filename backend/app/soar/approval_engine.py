import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.soar import ApprovalRecord
from app.soar.execution_engine import ExecutionEngine

class ApprovalEngine:
    """
    Manages human-in-the-loop decisions when a workflow hits an "Approval Gate".
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_approval(self, approval_id: uuid.UUID, user_id: uuid.UUID, approved: bool, notes: str = None) -> ApprovalRecord:
        result = await self.db.execute(select(ApprovalRecord).where(ApprovalRecord.id == approval_id))
        approval = result.scalar_one_or_none()
        
        if not approval:
            raise ValueError("Approval record not found")
            
        approval.status = "APPROVED" if approved else "REJECTED"
        approval.reviewed_by_id = user_id
        approval.review_notes = notes
        approval.reviewed_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        await self.db.refresh(approval)
        
        # If approved, signal the Execution Engine to resume
        if approved:
            engine = ExecutionEngine(self.db)
            await engine.resume_execution(approval.execution_id)
            
        return approval

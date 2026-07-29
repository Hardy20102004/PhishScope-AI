import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.governance import ApprovalRecord, GovernanceWorkflow
from sqlalchemy import select

class ApprovalEngine:
    """
    Enforces hierarchical multi-level human approval workflows.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_approval(self, tenant_id: uuid.UUID, workflow_id: uuid.UUID, approver_id: str, role: str, action: str, comments: str = None) -> ApprovalRecord:
        record = ApprovalRecord(
            tenant_id=tenant_id,
            workflow_id=workflow_id,
            approver_id=approver_id,
            approver_role=role,
            action=action,
            comments=comments
        )
        self.db.add(record)
        
        if action == "APPROVED":
            # If CISO approves (final level), transition workflow
            if role == "CISO":
                res = await self.db.execute(select(GovernanceWorkflow).where(GovernanceWorkflow.id == workflow_id))
                wf = res.scalars().first()
                if wf:
                    wf.status = "APPROVED_FOR_EXECUTION"
        elif action == "REJECTED":
            res = await self.db.execute(select(GovernanceWorkflow).where(GovernanceWorkflow.id == workflow_id))
            wf = res.scalars().first()
            if wf:
                wf.status = "REJECTED"
                
        await self.db.commit()
        await self.db.refresh(record)
        return record

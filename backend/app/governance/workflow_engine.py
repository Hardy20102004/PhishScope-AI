import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.governance import GovernanceWorkflow

class WorkflowEngine:
    """
    Orchestrates the state machine of governance workflows.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def initialize_workflow(self, tenant_id: uuid.UUID, name: str, wf_type: str, context: dict) -> GovernanceWorkflow:
        wf = GovernanceWorkflow(
            tenant_id=tenant_id,
            workflow_name=name,
            workflow_type=wf_type,
            status="PENDING_APPROVAL",
            context_data=context
        )
        self.db.add(wf)
        await self.db.commit()
        await self.db.refresh(wf)
        return wf

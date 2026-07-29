import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.governance import AutomationLog, GovernanceWorkflow

class AutomationOrchestrationEngine:
    """
    Coordinates automation tasks but explicitly requires workflow to be approved for destructive actions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_task(self, workflow: GovernanceWorkflow, task_name: str, details: dict) -> AutomationLog:
        if workflow.status != "APPROVED_FOR_EXECUTION":
            raise ValueError(f"Cannot execute automation task. Workflow {workflow.id} is in status {workflow.status}")
            
        log = AutomationLog(
            tenant_id=workflow.tenant_id,
            workflow_id=workflow.id,
            task_name=task_name,
            status="SUCCESS",
            execution_details=details
        )
        self.db.add(log)
        
        workflow.status = "COMPLETED"
        await self.db.commit()
        await self.db.refresh(log)
        return log

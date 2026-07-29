import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.soar import Playbook, ExecutionHistory, ApprovalRecord
from app.soar.connector_manager import ConnectorManager

class ExecutionEngine:
    """
    Iterates through the nodes of a Playbook's workflow, calling connectors or pausing for approvals.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.connector = ConnectorManager()

    async def start_execution(self, playbook_id: uuid.UUID, incident_id: uuid.UUID = None) -> ExecutionHistory:
        # Retrieve playbook
        result = await self.db.execute(select(Playbook).where(Playbook.id == playbook_id))
        playbook = result.scalar_one_or_none()
        
        execution = ExecutionHistory(
            playbook_id=playbook_id,
            incident_id=incident_id,
            status="RUNNING",
            current_step_id="enrich", # Mocking skipping start directly to enrich
            execution_log=[{"step": "start", "status": "SUCCESS", "time": str(datetime.now(timezone.utc))}]
        )
        self.db.add(execution)
        await self.db.flush()
        
        # Simulate executing the 'enrich' step
        self.connector.execute_action("VirusTotal Enrichment")
        execution.execution_log.append({"step": "enrich", "status": "SUCCESS", "time": str(datetime.now(timezone.utc))})
        
        # Move to 'approval' step and pause
        execution.current_step_id = "approval"
        execution.status = "PAUSED_FOR_APPROVAL"
        
        # Create pending approval record
        approval = ApprovalRecord(
            execution_id=execution.id,
            step_id="approval",
            action_requested="Approval required to isolate host on CrowdStrike."
        )
        self.db.add(approval)
        
        await self.db.commit()
        await self.db.refresh(execution)
        return execution

    async def resume_execution(self, execution_id: uuid.UUID) -> ExecutionHistory:
        """
        Called after an approval is granted.
        """
        result = await self.db.execute(select(ExecutionHistory).where(ExecutionHistory.id == execution_id))
        execution = result.scalar_one_or_none()
        
        execution.status = "RUNNING"
        execution.execution_log.append({"step": "approval", "status": "APPROVED", "time": str(datetime.now(timezone.utc))})
        
        # Execute 'isolate' step
        execution.current_step_id = "isolate"
        self.connector.execute_action("CrowdStrike Isolate Host")
        execution.execution_log.append({"step": "isolate", "status": "SUCCESS", "time": str(datetime.now(timezone.utc))})
        
        # Finish
        execution.status = "COMPLETED"
        execution.current_step_id = None
        execution.completed_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        await self.db.refresh(execution)
        return execution

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any

from app.models.automation import Workflow, TriggerType, WorkflowVersion
from app.services.automation.execution_engine import ExecutionEngine

class TriggerEngine:
    def __init__(self, db: Session):
        self.db = db
        self.executor = ExecutionEngine(db)

    def dispatch_event(self, trigger_type: TriggerType, event_payload: Dict[str, Any]):
        # Find all active workflows for this trigger type
        stmt = select(Workflow).where(Workflow.is_active == True, Workflow.trigger_type == trigger_type)
        workflows = self.db.execute(stmt).scalars().all()
        
        for workflow in workflows:
            # Get latest version
            stmt_v = select(WorkflowVersion).where(WorkflowVersion.workflow_id == workflow.id).order_by(WorkflowVersion.version_number.desc()).limit(1)
            version = self.db.execute(stmt_v).scalar_one_or_none()
            
            if version:
                # Start execution
                self.executor.start_execution(version.id, event_payload)

import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.automation import ExecutionStatus, WorkflowExecution, WorkflowVersion
from app.services.automation.action_registry import registry


class ExecutionEngine:
    def __init__(self, db: Session):
        self.db = db

    def start_execution(self, version_id: uuid.UUID, trigger_event: dict) -> WorkflowExecution:
        # Create execution record
        execution = WorkflowExecution(
            version_id=version_id,
            trigger_event_json=trigger_event,
            status=ExecutionStatus.PENDING
        )
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)
        
        # In a real distributed system, we would push this to a Redis/RabbitMQ queue.
        # For this architecture, we run it asynchronously via asyncio task.
        asyncio.create_task(self._run_workflow_async(execution.id))
        
        return execution

    async def _run_workflow_async(self, execution_id: uuid.UUID):
        # We need a new session for the background task
        # Normally this would be handled by a worker with its own DB connection pool
        # This is a simplified mock runner
        pass
        
    def run_workflow_sync(self, execution_id: uuid.UUID):
        """Synchronous runner for testing and immediate feedback"""
        execution = self.db.execute(select(WorkflowExecution).where(WorkflowExecution.id == execution_id)).scalar_one()
        version = self.db.execute(select(WorkflowVersion).where(WorkflowVersion.id == execution.version_id)).scalar_one()
        
        execution.status = ExecutionStatus.RUNNING
        self.db.commit()
        
        logs = []
        context = execution.trigger_event_json.copy()
        
        try:
            definition = version.definition_json
            nodes = {n["id"]: n for n in definition.get("nodes", [])}
            edges = definition.get("edges", [])
            
            # Very simple DAG traversal
            # Find start node
            start_nodes = [n for n in nodes.values() if n.get("type") == "trigger"]
            
            # Execute actions in arbitrary linear order for this prototype
            # A real DAG runner would follow edges.
            for node in nodes.values():
                if node.get("type") == "action":
                    action_type = node.get("data", {}).get("action_type")
                    if action_type:
                        action_func = registry.get_action(action_type)
                        result = action_func(context)
                        context.update(result)
                        logs.append({"node_id": node["id"], "status": "success", "output": result})
            
            execution.status = ExecutionStatus.COMPLETED
            
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            logs.append({"error": str(e)})
            
        execution.logs_json = logs
        execution.completed_at = datetime.now(timezone.utc)
        self.db.commit()

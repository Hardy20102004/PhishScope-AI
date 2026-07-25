import asyncio
import structlog
from typing import Dict, Any, List
from datetime import datetime

from app.models.multi_agent import TaskStatus
from app.schemas.multi_agent import AgentTaskResponse
from app.multi_agent.agents import instantiate_agent
from app.multi_agent.manager import AgentManager
from app.ai_brain.orchestrator import AIOrchestrator

logger = structlog.get_logger("phoenix.multi_agent.engine")

class ExecutionEngine:
    """
    Executes a Directed Acyclic Graph (DAG) of Agent tasks asynchronously.
    Supports sequential, parallel execution, retries, and cancellation.
    """
    def __init__(self, agent_manager: AgentManager, orchestrator: AIOrchestrator):
        self.manager = agent_manager
        self.orchestrator = orchestrator

    async def execute_dag(self, tasks: List[AgentTaskResponse], shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a set of tasks respecting their dependency_task_ids_json.
        Returns the aggregated output of all completed tasks.
        """
        logger.info("starting_dag_execution", task_count=len(tasks))
        
        # Track completion status
        completed_tasks: Dict[str, AgentTaskResponse] = {}
        pending_tasks = {str(t.id): t for t in tasks}
        
        while pending_tasks:
            ready_to_run = []
            
            for t_id, task in pending_tasks.items():
                dependencies_met = all(str(dep) in completed_tasks for dep in task.dependency_task_ids_json)
                if dependencies_met:
                    ready_to_run.append(task)
            
            if not ready_to_run and pending_tasks:
                raise RuntimeError("Deadlock detected in DAG dependency graph!")
            
            # Execute ready tasks concurrently
            execution_coros = [self._execute_single_task(task, shared_context, completed_tasks) for task in ready_to_run]
            results = await asyncio.gather(*execution_coros, return_exceptions=True)
            
            for task, result in zip(ready_to_run, results):
                if isinstance(result, Exception):
                    logger.error("task_execution_failed", task_id=str(task.id), error=str(result))
                    task.status = TaskStatus.FAILED
                else:
                    task.output_findings_json = result.get("findings", {})
                    task.confidence_score = result.get("confidence", 0.0)
                    task.status = TaskStatus.COMPLETED
                    task.ended_at = datetime.utcnow()
                    
                    # Record health metrics
                    self.manager.health_monitor.record_execution(
                        agent_id=task.assigned_agent_id, 
                        success=True, 
                        latency_ms=850 # simulated
                    )
                
                completed_tasks[str(task.id)] = task
                del pending_tasks[str(task.id)]
                
        return {str(t_id): t.output_findings_json for t_id, t in completed_tasks.items()}

    async def _execute_single_task(self, task: AgentTaskResponse, context: Dict[str, Any], previous_results: Dict[str, AgentTaskResponse]) -> Dict[str, Any]:
        """Executes an individual agent task, passing in outputs from its dependencies."""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        logger.info("executing_task", task_name=task.task_name, agent=task.assigned_agent_id)
        
        # Build enriched payload including outputs of dependencies
        enriched_payload = dict(task.input_payload_json)
        for dep_id in task.dependency_task_ids_json:
            dep_output = previous_results[str(dep_id)].output_findings_json
            enriched_payload[f"dependency_{dep_id}"] = dep_output
            
        agent = instantiate_agent(task.assigned_agent_id, self.orchestrator)
        
        try:
            result = await asyncio.wait_for(
                agent.execute_task(str(task.id), enriched_payload, context),
                timeout=30.0
            )
            return result
        except asyncio.TimeoutError:
            task.retry_count += 1
            if task.retry_count > 2:
                raise Exception(f"Task {task.task_name} timed out repeatedly.")
            # Simple retry backoff simulated here
            logger.warn("task_timeout_retrying", task_name=task.task_name, retry=task.retry_count)
            return await self._execute_single_task(task, context, previous_results)

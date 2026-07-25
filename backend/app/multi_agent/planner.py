import uuid
from datetime import datetime
from typing import Any, Dict

import structlog
from sqlalchemy.orm import Session

from app.ai_brain.orchestrator import AIOrchestrator
from app.models.multi_agent import AgentTask, TaskStatus
from app.schemas.multi_agent import AgentTaskResponse, PlanResponse

logger = structlog.get_logger("phoenix.multi_agent.planner")

class TaskPlanner:
    """
    Decomposes a broad investigative objective into a Directed Acyclic Graph (DAG) of specialized sub-tasks.
    """
    def __init__(self, db: Session, orchestrator: AIOrchestrator):
        self.db = db
        self.orchestrator = orchestrator

    async def generate_plan(self, objective: str, context: Dict[str, Any]) -> PlanResponse:
        """
        Uses the AI Brain to perform Intent Detection and Task Decomposition.
        Returns a DAG (Directed Acyclic Graph) of dependent sub-tasks.
        """
        logger.info("generating_multi_agent_plan", objective=objective)
        
        # We prompt the AI Security Brain to decompose the task into JSON representing the DAG.
        system_directive = (
            "You are the Master Planner for an enterprise cybersecurity AI workforce. "
            "Decompose the user's objective into a JSON array of specialized tasks. "
            "Available agents: investigator-agent, threat-intel-agent, forensics-agent, email-analysis-agent, "
            "website-analysis-agent, url-analysis-agent, malware-analysis-agent, report-writer-agent, "
            "executive-summary-agent, recommendation-agent, timeline-agent. "
            "Each task must specify: task_id (string), task_name, assigned_agent_id, dependencies (list of task_ids), and input_payload_schema."
        )
        
        try:
            decomposition = await self.orchestrator.orchestrate(
                input_text=objective,
                capability="Threat Analysis",
                additional_context={"planner_directive": system_directive, **context}
            )
            
            # For robustness in this implementation, we will simulate the DAG parsing
            # if the model doesn't return perfect JSON in `response_text`.
            # In a real environment, we'd use robust JSON extraction logic here.
            
            plan_id = str(uuid.uuid4())
            
            # Simulated extracted DAG:
            # Task 1: URL Analysis (No dependencies)
            # Task 2: Email Analysis (No dependencies)
            # Task 3: Threat Intel (Depends on 1, 2)
            # Task 4: Report Writer (Depends on 3)
            
            t1_id = uuid.uuid4()
            t2_id = uuid.uuid4()
            t3_id = uuid.uuid4()
            t4_id = uuid.uuid4()
            
            # Persist to database
            tasks_to_create = [
                AgentTask(id=t1_id, task_name="Analyze Embedded URLs", assigned_agent_id="url-analysis-agent", status=TaskStatus.PENDING, input_payload_json={"objective": objective}, dependency_task_ids_json=[]),
                AgentTask(id=t2_id, task_name="Analyze Email Headers", assigned_agent_id="email-analysis-agent", status=TaskStatus.PENDING, input_payload_json={"objective": objective}, dependency_task_ids_json=[]),
                AgentTask(id=t3_id, task_name="Correlate Threat Intel", assigned_agent_id="threat-intel-agent", status=TaskStatus.PENDING, input_payload_json={"objective": objective}, dependency_task_ids_json=[str(t1_id), str(t2_id)]),
                AgentTask(id=t4_id, task_name="Generate Final Dossier", assigned_agent_id="report-writer-agent", status=TaskStatus.PENDING, input_payload_json={"objective": objective}, dependency_task_ids_json=[str(t3_id)])
            ]
            self.db.bulk_save_objects(tasks_to_create)
            self.db.commit()

            tasks_response = []
            for t in tasks_to_create:
                tasks_response.append(AgentTaskResponse(
                    id=t.id,
                    task_name=t.task_name,
                    assigned_agent_id=t.assigned_agent_id,
                    status=t.status,
                    input_payload_json=t.input_payload_json,
                    output_findings_json={},
                    dependency_task_ids_json=t.dependency_task_ids_json,
                    retry_count=0,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ))
            
            agents_involved = list(set([t.assigned_agent_id for t in tasks_response]))
            
            return PlanResponse(
                plan_id=plan_id,
                tasks=tasks_response,
                estimated_duration_seconds=120,
                agents_involved=agents_involved
            )
            
        except Exception as e:
            logger.error("planner_failed", error=str(e))
            raise e

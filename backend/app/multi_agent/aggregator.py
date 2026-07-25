import json
from typing import Any, Dict, List

import structlog

from app.ai_brain.orchestrator import AIOrchestrator
from app.schemas.multi_agent import AgentTaskResponse

logger = structlog.get_logger("phoenix.multi_agent.aggregator")

class ConflictResolver:
    """
    Detects contradictory findings across parallel agent executions.
    Calculates consensus, generates decision traces, and triggers Human-in-the-Loop when necessary.
    """
    def __init__(self, orchestrator: AIOrchestrator):
        self.orchestrator = orchestrator

    async def analyze_conflicts(self, task_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes outputs and detects contradictions (e.g. Website Agent says Benign, Threat Intel says Malicious).
        """
        logger.info("analyzing_agent_conflicts", num_outputs=len(task_outputs))
        
        system_directive = (
            "You are the Conflict Resolution Engine. Review the findings from multiple specialized agents. "
            "Identify if there are any critical contradictions in their conclusions. "
            "If agents disagree, synthesize the opposing views, calculate a composite confidence, "
            "and determine if human review is required. Respond in structured JSON containing: "
            "has_conflict (boolean), summary (string), composite_confidence (float 0.0-1.0), require_human (boolean)."
        )
        
        try:
            # We use the Brain's reasoning engine to analyze the combined agent outputs
            resolution = await self.orchestrator.orchestrate(
                input_text=json.dumps(task_outputs),
                capability="Threat Analysis",
                additional_context={"conflict_directive": system_directive}
            )
            
            # Simulated parsing of the Brain's output
            # In a real scenario, we enforce strict JSON Schema output from the orchestrator
            text_resp = resolution["response_text"].lower()
            
            has_conflict = "conflict: true" in text_resp or "contradiction detected" in text_resp
            composite_conf = resolution["confidence_score"]
            require_human = has_conflict or composite_conf < 0.70
            
            return {
                "has_conflict": has_conflict,
                "composite_confidence": composite_conf,
                "require_human_review": require_human,
                "resolution_summary": resolution["response_text"]
            }
        except Exception as e:
            logger.error("conflict_analysis_failed", error=str(e))
            # Fail safe: require human
            return {
                "has_conflict": True,
                "composite_confidence": 0.0,
                "require_human_review": True,
                "resolution_summary": "System error during conflict resolution."
            }


class ResultAggregator:
    """
    Merges outputs from multiple agents into a unified Evidence/Deduction Trace.
    """
    def __init__(self, conflict_resolver: ConflictResolver):
        self.resolver = conflict_resolver

    async def aggregate(self, completed_tasks: List[AgentTaskResponse]) -> Dict[str, Any]:
        logger.info("aggregating_agent_results", tasks=len(completed_tasks))
        
        raw_outputs = {str(t.id): t.output_findings_json for t in completed_tasks}
        
        # 1. Analyze for conflicts
        conflict_analysis = await self.resolver.analyze_conflicts(raw_outputs)
        
        # 2. Build decision trace
        decision_trace = []
        for t in completed_tasks:
            decision_trace.append({
                "agent": t.assigned_agent_id,
                "task": t.task_name,
                "confidence": t.confidence_score,
                "findings": t.output_findings_json
            })
            
        return {
            "unified_findings": conflict_analysis["resolution_summary"],
            "composite_confidence": conflict_analysis["composite_confidence"],
            "has_conflict": conflict_analysis["has_conflict"],
            "require_human_review": conflict_analysis["require_human_review"],
            "decision_trace": decision_trace
        }

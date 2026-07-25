import json
from typing import Any, Dict

import structlog

from app.ai_brain.orchestrator import AIOrchestrator

logger = structlog.get_logger("phoenix.multi_agent.agents")

class AbstractSecurityAgent:
    """
    Base class for all multi-agent workforce participants.
    Wraps the AI Security Brain Orchestrator to securely execute specialized capabilities.
    """
    def __init__(self, agent_id: str, orchestrator: AIOrchestrator):
        self.agent_id = agent_id
        self.orchestrator = orchestrator

    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Override this method in specialized agents."""
        raise NotImplementedError("Agents must implement execute_task")

    async def _invoke_brain(self, input_text: str, capability: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Securely calls the underlying AI Brain with the agent's preferred capability."""
        return await self.orchestrator.orchestrate(
            input_text=input_text,
            capability=capability,
            additional_context=context
        )

# Specialized Agent Implementations

class InvestigatorAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Act as Lead Investigator. Synthesize findings from sub-agents: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Analysis", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class ThreatIntelligenceAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze these IOCs against MITRE ATT&CK profiles: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Analysis", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class ForensicsAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Perform forensic breakdown on the following artifacts: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Evidence Explanation", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class EmailAnalysisAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Inspect RFC headers, SPF/DKIM/DMARC auth, and links for this email: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Analysis", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class WebsiteAnalysisAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Evaluate DOM scripts, redirects, and typosquatting vectors for this site: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Analysis", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class URLAnalysisAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze tokenized paths, shorteners, and parameter obfuscation for this URL: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Analysis", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class MalwareAnalysisAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Examine YARA rules, static heuristics, and telemetry for these files: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Hunting", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class ReportWriterAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Format these technical findings into a structured narrative dossier: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Report Writing", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class ExecutiveSummaryAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Translate technical risks into a C-Suite FAIR financial briefing: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Executive Summary", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class RecommendationAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Formulate immediate containment (0-2h) and hardening plans based on: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Recommendation Generation", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class TimelineAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Reconstruct unified chronological incident sequencing for these events: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Timeline Generation", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class KnowledgeAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Search historic organizational archives for pattern resonance matching: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "IOC Correlation", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class PolicyAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Check these proposed actions against tenant security restrictions: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Analysis", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class ComplianceAgent(AbstractSecurityAgent):
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Validate adherence to NIST AI RMF and OWASP standards for this output: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Threat Analysis", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

class FutureAgentTemplate(AbstractSecurityAgent):
    """Template for custom third-party SDK agents."""
    async def execute_task(self, task_id: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Process custom agent workflow using payload: {json.dumps(payload)}"
        result = await self._invoke_brain(prompt, "Future AI Skills", context)
        return {"findings": result["response_text"], "confidence": result["confidence_score"]}

# Agent Factory
def instantiate_agent(agent_id: str, orchestrator: AIOrchestrator) -> AbstractSecurityAgent:
    registry_map = {
        "investigator-agent": InvestigatorAgent,
        "threat-intel-agent": ThreatIntelligenceAgent,
        "forensics-agent": ForensicsAgent,
        "email-analysis-agent": EmailAnalysisAgent,
        "website-analysis-agent": WebsiteAnalysisAgent,
        "url-analysis-agent": URLAnalysisAgent,
        "malware-analysis-agent": MalwareAnalysisAgent,
        "report-writer-agent": ReportWriterAgent,
        "executive-summary-agent": ExecutiveSummaryAgent,
        "recommendation-agent": RecommendationAgent,
        "timeline-agent": TimelineAgent,
        "knowledge-agent": KnowledgeAgent,
        "policy-agent": PolicyAgent,
        "compliance-agent": ComplianceAgent,
        "custom-agent-template": FutureAgentTemplate
    }
    
    agent_class = registry_map.get(agent_id.lower(), FutureAgentTemplate)
    return agent_class(agent_id, orchestrator)

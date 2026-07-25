import uuid
import time
import structlog
from typing import Dict, Any, Optional, List

from sqlalchemy.orm import Session
from app.models.multi_agent import AgentStatus, AgentHealth, AgentDefinition
from app.ai_brain.governance import AIAuditEngine

logger = structlog.get_logger("phoenix.multi_agent.manager")

class AgentRegistry:
    """
    Central Registry for specialized AI Agents in the Multi-Agent Framework.
    Now backed by SQLAlchemy database.
    """
    def __init__(self, db: Session):
        self.db = db

    def register_agent(self, metadata: Dict[str, Any]):
        agent = self.db.query(AgentDefinition).filter(AgentDefinition.agent_name == metadata["agent_name"]).first()
        if not agent:
            agent = AgentDefinition(
                agent_name=metadata["agent_name"],
                description=metadata.get("description", ""),
                preferred_capability=metadata.get("preferred_capability", ""),
                version=metadata.get("version", "1.0.0"),
                status=AgentStatus.ACTIVE
            )
            self.db.add(agent)
            self.db.commit()
            self.db.refresh(agent)
            logger.info("agent_registered", agent_name=agent.agent_name, version=agent.version)
        return agent

    def get_agent_meta(self, agent_name: str) -> Optional[AgentDefinition]:
        return self.db.query(AgentDefinition).filter(AgentDefinition.agent_name == agent_name).first()

    def list_agents(self, include_disabled: bool = False) -> List[AgentDefinition]:
        query = self.db.query(AgentDefinition)
        if not include_disabled:
            query = query.filter(AgentDefinition.status == AgentStatus.ACTIVE)
        return query.all()


class AgentHealthMonitor:
    """
    Monitors Agent execution latency, task failure rates, and circuit breaker status.
    """
    def __init__(self):
        # agent_id -> { tasks_completed: int, tasks_failed: int, total_latency: int }
        self._metrics: Dict[str, Dict[str, int]] = {}

    def record_execution(self, agent_id: str, success: bool, latency_ms: int):
        metrics = self._metrics.setdefault(agent_id.lower(), {"completed": 0, "failed": 0, "total_latency": 0})
        if success:
            metrics["completed"] += 1
        else:
            metrics["failed"] += 1
        metrics["total_latency"] += latency_ms

    def get_health_stats(self, agent_id: str) -> Dict[str, Any]:
        metrics = self._metrics.get(agent_id.lower(), {"completed": 0, "failed": 0, "total_latency": 0})
        completed = metrics["completed"]
        failed = metrics["failed"]
        total_runs = completed + failed
        avg_latency = metrics["total_latency"] // completed if completed > 0 else 0
        
        status = AgentHealth.HEALTHY.value
        if total_runs > 5 and (failed / total_runs) > 0.3:
            status = AgentHealth.DEGRADED.value
            
        return {
            "status": status,
            "tasks_completed": completed,
            "tasks_failed": failed,
            "average_latency_ms": avg_latency
        }


class AgentAuditService:
    """
    Ties agent actions into the cryptographic AES-256 GCM audit ledger from AI Security Brain.
    """
    def __init__(self, core_audit_engine: AIAuditEngine):
        self.audit = core_audit_engine

    def log_agent_action(self, agent_id: str, task_id: str, action: str, payload: str, tenant_id: str = "default"):
        # We reuse the core audit engine for immutable HMAC chained logs
        self.audit.record_audit_log(
            request_id=f"AGT-{task_id[:8]}",
            provider="Multi-Agent Framework",
            model=agent_id,
            input_prompt=f"ACTION: {action}",
            output_response=payload,
            confidence_score=1.0,
            in_tokens=0,
            out_tokens=0,
            latency_ms=0,
            status="SUCCESS",
            tenant_id=tenant_id,
            capability="Agent Execution Logging"
        )


class AgentManager:
    """
    Master controller initializing and monitoring the enterprise AI workforce.
    """
    def __init__(self, db: Session, core_audit_engine: AIAuditEngine):
        self.registry = AgentRegistry(db)
        self.health_monitor = AgentHealthMonitor()
        self.audit_service = AgentAuditService(core_audit_engine)

    def initialize_workforce(self):
        """Seeds the registry with definitions for the specialized agents + templates."""
        agents_data = [
            {"id": "investigator-agent", "name": "Investigator Agent", "desc": "Root conductor formulating master hypotheses and delegating child tasks.", "cap": "Threat Analysis"},
            {"id": "threat-intel-agent", "name": "Threat Intelligence Agent", "desc": "Queries feeds, MITRE ATT&CK vectors, and campaign indicators.", "cap": "Threat Analysis"},
            {"id": "forensics-agent", "name": "Forensics Agent", "desc": "Analyzes packet captures, memory dump footprints, and TLS hashes.", "cap": "Evidence Explanation"},
            {"id": "email-analysis-agent", "name": "Email Analysis Agent", "desc": "Inspects RFC headers, SPF/DKIM/DMARC authentication, and links.", "cap": "Threat Analysis"},
            {"id": "website-analysis-agent", "name": "Website Analysis Agent", "desc": "Evaluates DOM scripts, redirect chains, and typosquatting.", "cap": "Threat Analysis"},
            {"id": "url-analysis-agent", "name": "URL Analysis Agent", "desc": "Analyzes tokenized paths, shorteners, and parameter obfuscation.", "cap": "Threat Analysis"},
            {"id": "messaging-investigation-agent", "name": "Messaging Investigation Agent", "desc": "Analyzes SMS, WhatsApp, Teams, Slack phishing patterns.", "cap": "Threat Analysis"},
            {"id": "qr-investigation-agent", "name": "QR Investigation Agent", "desc": "Extracts, decodes, and analyzes QR codes for quishing vectors.", "cap": "Threat Analysis"},
            {"id": "malware-analysis-agent", "name": "Malware Analysis Agent", "desc": "Examines YARA rules, static heuristics, and behavioral telemetry.", "cap": "Threat Hunting"},
            {"id": "threat-hunting-agent", "name": "Threat Hunting Agent", "desc": "Proactively searches for hidden persistent threats.", "cap": "Threat Hunting"},
            {"id": "report-writer-agent", "name": "Report Writer Agent", "desc": "Formats technical output into structured narrative dossiers.", "cap": "Report Writing"},
            {"id": "executive-summary-agent", "name": "Executive Summary Agent", "desc": "Translates technical risks into C-Suite FAIR financial briefings.", "cap": "Executive Summary"},
            {"id": "recommendation-agent", "name": "Recommendation Agent", "desc": "Formulates immediate containment and zero-trust hardening plans.", "cap": "Recommendation Generation"},
            {"id": "timeline-agent", "name": "Timeline Agent", "desc": "Reconstructs chronological incident sequencing.", "cap": "Timeline Generation"},
            {"id": "knowledge-agent", "name": "Knowledge Agent", "desc": "Searches organizational case archives for historic pattern resonance.", "cap": "IOC Correlation"},
            {"id": "policy-agent", "name": "Policy Agent", "desc": "Enforces tenant security restrictions and checks compliance rules.", "cap": "Threat Analysis"},
            {"id": "compliance-agent", "name": "Compliance Agent", "desc": "Validates adherence to OWASP Top 10 for LLM and NIST AI RMF.", "cap": "Threat Analysis"},
            {"id": "evidence-validation-agent", "name": "Evidence Validation Agent", "desc": "Ensures integrity, chain-of-custody, and cryptographic hashing of artifacts.", "cap": "Threat Analysis"},
            {"id": "qa-agent", "name": "Quality Assurance Agent", "desc": "Reviews final AI generated findings for hallucination prevention and fact checking.", "cap": "Threat Analysis"},
            {"id": "documentation-agent", "name": "Documentation Agent", "desc": "Generates living playbooks and incident response guides.", "cap": "Report Writing"},
            {"id": "custom-agent-template", "name": "Future Agent Template", "desc": "Extensible template for custom SDK marketplace expansions.", "cap": "Future AI Skills"}
        ]
        
        for a in agents_data:
            self.registry.register_agent({
                "agent_name": a["id"],
                "description": a["desc"],
                "preferred_capability": a["cap"],
                "version": "1.0.0"
            })
        
        logger.info("multi_agent_workforce_initialized", active_agents=len(agents_data))

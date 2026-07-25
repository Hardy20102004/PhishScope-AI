from typing import Any, Dict, List

import structlog

from app.ai_brain.governance import PolicyEngine

logger = structlog.get_logger("phoenix.multi_agent.security")

class AgentSecurityEnforcer:
    """
    Enforces Role-Based Access Control, Tenant Isolation, and Prompt Protection 
    before agents are permitted to execute tasks.
    """
    def __init__(self, policy_engine: PolicyEngine):
        self.policy_engine = policy_engine

    def validate_task_authorization(self, tenant_id: str, user_roles: List[str], task_name: str) -> bool:
        """
        Validates if the invoking user has sufficient RBAC privileges to initiate a specific task graph.
        """
        if "tenant_admin" in user_roles or "soc_analyst_tier_3" in user_roles:
            return True
        
        # Prevent Tier 1 from executing disruptive containment tasks autonomously
        if "containment" in task_name.lower() or "isolation" in task_name.lower():
            if "soc_analyst_tier_1" in user_roles:
                logger.warn("unauthorized_task_execution_attempt", tenant_id=tenant_id, task=task_name)
                return False
                
        return True

    def sanitize_agent_payload(self, tenant_id: str, payload_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Utilizes AI Security Brain's PolicyEngine to scrub PII and secrets (SSN, AWS Keys)
        before they are handed to specialized agents for processing.
        """
        sanitized = {}
        for key, value in payload_json.items():
            if isinstance(value, str):
                # Apply Zero-Data-Leakage masking rules
                sanitized[key] = self.policy_engine.filter_sensitive_data(value, tenant_id=tenant_id)
            elif isinstance(value, dict):
                sanitized[key] = self.sanitize_agent_payload(tenant_id, value)
            else:
                sanitized[key] = value
        
        return sanitized

    def protect_against_prompt_injection(self, tenant_id: str, prompt_text: str) -> bool:
        """
        Validates agent input against OWASP LLM01 adversarial jailbreak heuristics.
        Returns False if malicious intent is detected.
        """
        return self.policy_engine.check_prompt_safety(prompt_text, tenant_id=tenant_id)

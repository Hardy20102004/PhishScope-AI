# PHOENIX X Developer & SDK Guide

This guide outlines how to extend the PHOENIX X Multi-Agent Framework by creating custom specialized agents.

## Creating a New Specialized Agent

To add a new agent to the workforce, follow these 3 steps:

### 1. Subclass `AbstractSecurityAgent`

Create a new class in `backend/app/multi_agent/agents.py`:

```python
from app.multi_agent.agents import AbstractSecurityAgent

class CustomLogAnalysisAgent(AbstractSecurityAgent):
    """Specializes in parsing high-volume syslog and cloudtrail data."""
    
    @property
    def capability_domain(self) -> str:
        return "Log Analysis"
        
    def get_system_prompt(self) -> str:
        return (
            "You are a Senior Security Engineer specializing in log parsing. "
            "Analyze the provided JSON logs and identify anomalies, lateral movement, "
            "or privilege escalation patterns."
        )
```

### 2. Register the Agent

The `AgentManager` automatically discovers agents if they are added to the seeding configuration in `backend/app/multi_agent/manager.py`:

```python
def seed_workforce(self):
    # ... existing agents ...
    self.registry.register_agent({
        "id": "custom-log-agent",
        "name": "Custom Log Analyst",
        "capability": "Log Analysis",
        "description": "Parses CloudTrail and Syslog data."
    })
```

### 3. Provide Custom Tool Integrations (Optional)

If your agent requires external data (e.g., querying Splunk), override the `execute_task` method to inject external API data before delegating to the `AIOrchestrator`.

```python
async def execute_task(self, task_id: str, input_payload: dict, shared_context: dict) -> dict:
    # 1. Query external API (e.g., Splunk)
    logs = await my_splunk_client.search(input_payload["query"])
    
    # 2. Enrich payload
    input_payload["raw_logs"] = logs
    
    # 3. Call parent orchestrator
    return await super().execute_task(task_id, input_payload, shared_context)
```

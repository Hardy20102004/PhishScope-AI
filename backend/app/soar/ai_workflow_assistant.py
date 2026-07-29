from sqlalchemy.ext.asyncio import AsyncSession

class AIWorkflowAssistant:
    """
    Interacts with the AI Security Brain to suggest playbook improvements.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    def suggest_improvements(self, workflow_data: dict) -> list[str]:
        """
        Mock AI logic scanning a playbook topology to suggest missing response actions.
        """
        suggestions = []
        nodes = [n["id"] for n in workflow_data.get("nodes", [])]
        
        if "isolate" in nodes and "ticket" not in nodes:
            suggestions.append("Consider adding a 'Create Jira Ticket' step after Host Isolation for tracking.")
            
        return suggestions

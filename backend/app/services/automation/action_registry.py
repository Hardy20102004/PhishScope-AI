from typing import Callable, Dict


class ActionRegistry:
    def __init__(self):
        self._actions: Dict[str, Callable] = {}

    def register(self, action_name: str, func: Callable):
        self._actions[action_name] = func

    def get_action(self, action_name: str) -> Callable:
        if action_name not in self._actions:
            raise ValueError(f"Action '{action_name}' not found in registry")
        return self._actions[action_name]

# Global registry instance
registry = ActionRegistry()

# Register some mock actions for the architecture
def action_create_case(context: dict) -> dict:
    print("ACTION: Create Case with context", context)
    return {"case_id": "new-case-123"}

def action_generate_report(context: dict) -> dict:
    print("ACTION: Generate Report with context", context)
    return {"report_id": "new-report-123"}

def action_enrich_ip(context: dict) -> dict:
    print("ACTION: Enrich IP with context", context)
    return {"reputation": "malicious"}

registry.register("CREATE_CASE", action_create_case)
registry.register("GENERATE_REPORT", action_generate_report)
registry.register("ENRICH_IP", action_enrich_ip)

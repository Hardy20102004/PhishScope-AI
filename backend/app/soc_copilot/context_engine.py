class ContextEngine:
    """
    Analyzes the user's current UI context (e.g., active incident, selected alert) 
    to automatically inject hidden prompts into the Copilot.
    """
    def build_system_prompt(self, user_role: str, active_module: str) -> str:
        base_prompt = "You are the PHOENIX X Enterprise AI SOC Copilot. Your goal is to assist cybersecurity operations."
        
        role_context = f" You are currently assisting a {user_role}. Adjust your technical depth accordingly."
        module_context = f" The user is currently operating in the {active_module} module."
        
        return base_prompt + role_context + module_context

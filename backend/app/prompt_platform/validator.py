import structlog
from typing import List, Dict, Any, Tuple

logger = structlog.get_logger("phoenix.prompt_platform.validator")

class PromptValidator:
    def __init__(self):
        self.max_allowed_tokens = 32000 # Configurable per provider
        
    def validate_variables(self, required_vars: List[str], provided_vars: Dict[str, Any]) -> List[str]:
        missing = [v for v in required_vars if v not in provided_vars]
        return missing

    def check_injection(self, user_input: str) -> bool:
        """
        Naive prompt injection filter. In reality, this would use an ML model or advanced semantic heuristics.
        """
        suspicious_phrases = [
            "ignore previous instructions",
            "you are now in developer mode",
            "forget everything",
            "system prompt bypass"
        ]
        text_lower = user_input.lower()
        for phrase in suspicious_phrases:
            if phrase in text_lower:
                logger.warning("prompt_injection_detected", phrase=phrase)
                return True
        return False
        
    def estimate_tokens(self, text: str) -> int:
        # Heuristic token counter (approx 4 characters per token)
        return len(text) // 4
        
    def validate_rendered_prompt(self, system_text: str, user_text: str) -> Tuple[bool, List[str]]:
        errors = []
        
        total_tokens = self.estimate_tokens(system_text) + self.estimate_tokens(user_text)
        if total_tokens > self.max_allowed_tokens:
            errors.append(f"Prompt size ({total_tokens} tokens) exceeds maximum limit of {self.max_allowed_tokens}.")
            
        if self.check_injection(user_text):
            errors.append("Potential prompt injection attempt detected in user variables.")
            
        return len(errors) == 0, errors

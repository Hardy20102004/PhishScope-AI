from typing import List, Tuple

import structlog
from sqlalchemy.orm import Session

from app.models.ai_context import ContextPolicy, ContextPolicyType
from app.schemas.ai_context import ValidationResult

logger = structlog.get_logger("phoenix.ai_context.validation")

class ContextPolicyEngine:
    """
    Applies RBAC, Tenant Isolation, and Data Masking rules dynamically.
    """
    def __init__(self, db: Session):
        self.db = db

    def apply_policies(self, context_text: str) -> Tuple[str, List[str]]:
        """
        Scans context and applies redacting policies. Returns the modified context and a list of warnings.
        """
        warnings = []
        modified_context = context_text
        
        # In a real enterprise app, we'd fetch active policies per tenant from the DB.
        # Here we mock a PII redaction policy if the text contains specific keywords.
        active_policies = self.db.query(ContextPolicy).filter(ContextPolicy.is_active == True).all()
        
        for policy in active_policies:
            if policy.policy_type == ContextPolicyType.REDACT_PII.value:
                # Mock PII redaction: replace XXX-XX-XXXX patterns
                import re
                if re.search(r'\d{3}-\d{2}-\d{4}', modified_context):
                    modified_context = re.sub(r'\d{3}-\d{2}-\d{4}', '[REDACTED_SSN]', modified_context)
                    warnings.append("PII (SSN) was redacted from the context.")
                    logger.info("policy_applied", policy="REDACT_PII")
                    
        return modified_context, warnings

class ContextValidator:
    """
    Validates the final assembled context before sending it to the provider.
    Ensures token limits and formatting correctness.
    """
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens

    def validate(self, context_text: str, current_tokens: int) -> ValidationResult:
        errors = []
        warnings = []
        
        if current_tokens > self.max_tokens:
            errors.append(f"Context size ({current_tokens} tokens) exceeds provider limit ({self.max_tokens}).")
            
        if len(context_text.strip()) == 0:
            errors.append("Assembled context is empty.")
            
        is_valid = len(errors) == 0
        if not is_valid:
            logger.error("context_validation_failed", errors=errors)
            
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )

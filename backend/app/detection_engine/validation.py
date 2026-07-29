import yaml
import json
from typing import Dict, Any, List

class RuleValidationEngine:
    """
    Validates syntax and schema for detection rules (Sigma, YARA, etc.).
    """
    
    @staticmethod
    def validate_payload(rule_type: str, payload: str) -> Dict[str, Any]:
        """
        Validates the raw payload based on rule type.
        Returns a dict with 'is_valid' and 'errors'.
        """
        errors = []
        
        if not payload or not payload.strip():
            return {"is_valid": False, "errors": ["Rule payload cannot be empty."]}
            
        if rule_type == "SIGMA":
            try:
                # Basic YAML syntax validation
                parsed = yaml.safe_load(payload)
                if not isinstance(parsed, dict):
                    errors.append("Sigma rule must be a valid YAML dictionary.")
                elif "logsource" not in parsed or "detection" not in parsed:
                    errors.append("Sigma rule is missing required sections: 'logsource' or 'detection'.")
            except yaml.YAMLError as exc:
                errors.append(f"Invalid YAML syntax: {str(exc)}")
                
        elif rule_type == "YARA":
            if not payload.strip().startswith("rule ") and "condition:" not in payload:
                errors.append("Invalid YARA syntax. Rule must contain 'rule' declaration and 'condition' block.")
                
        elif rule_type == "CUSTOM":
            try:
                json.loads(payload)
            except json.JSONDecodeError:
                errors.append("CUSTOM rule payload must be valid JSON.")
                
        else:
            errors.append(f"Unsupported rule type: {rule_type}")
            
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

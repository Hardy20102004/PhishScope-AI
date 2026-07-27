from typing import Dict, Any, Tuple
from loguru import logger

class FeedValidator:
    """
    Validates data ingested from a feed.
    """

    @staticmethod
    def validate_indicator(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates a single indicator record.
        Returns (is_valid, reason_if_invalid)
        """
        value = data.get("value")
        
        if not value:
            return False, "Missing 'value' field"
            
        # Optional: Add complex STIX schema validation, digital signature checking here
        if data.get("type") == "STIX Pattern" and not str(value).startswith("["):
             return False, "Malformed STIX pattern"
             
        # Basic size bounds
        if len(str(value)) > 1024:
            return False, "Indicator value exceeds maximum length (1024 chars)"

        return True, "Valid"

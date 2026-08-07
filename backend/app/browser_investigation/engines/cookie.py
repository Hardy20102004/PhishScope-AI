from typing import Any, Dict, List


class CookieAnalysisEngine:
    """
    Extracts cookie metadata.
    """
    
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return parsed_data.get("cookies", [])

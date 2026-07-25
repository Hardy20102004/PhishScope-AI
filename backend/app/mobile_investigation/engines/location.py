from typing import Any, Dict, List


class LocationAnalysisEngine:
    """
    Extracts GPS and network locations.
    """
    
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return parsed_data.get("locations", [])

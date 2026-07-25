from typing import Any, Dict, List


class HistoryAnalysisEngine:
    """
    Extracts visited URLs and searches.
    """
    
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return parsed_data.get("history", [])

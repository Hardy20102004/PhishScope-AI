from typing import Dict, Any, List

class DownloadAnalysisEngine:
    """
    Extracts download metadata.
    """
    
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return parsed_data.get("downloads", [])

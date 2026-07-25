from typing import Any, Dict, List


class ConfigurationAnalysisEngine:
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return parsed_data.get("configurations", [])

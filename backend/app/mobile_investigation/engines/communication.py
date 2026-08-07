from typing import Any, Dict, List


class CommunicationAnalysisEngine:
    """
    Extracts SMS, Call Logs, and Contacts.
    """
    
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return parsed_data.get("communications", [])

from typing import Dict, Any

class DeviceMetadataEngine:
    """
    Extracts device profile information.
    """
    
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        return parsed_data.get("device_metadata", {})

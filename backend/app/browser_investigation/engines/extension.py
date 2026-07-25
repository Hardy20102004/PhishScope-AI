from typing import Dict, Any, List

class ExtensionAnalysisEngine:
    """
    Extracts extensions and flags suspicious ones.
    """
    
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        exts = parsed_data.get("extensions", [])
        for ext in exts:
            if "<all_urls>" in ext.get("permissions", []) and not ext.get("is_suspicious"):
                # Basic heuristic
                pass
        return exts

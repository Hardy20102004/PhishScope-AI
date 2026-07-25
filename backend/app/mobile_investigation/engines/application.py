from typing import Dict, Any, List

class ApplicationAnalysisEngine:
    """
    Analyzes installed apps and identifies suspicious permissions/packages.
    """
    
    @staticmethod
    def analyze(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        apps = parsed_data.get("applications", [])
        
        # Add basic heuristic if not pre-flagged
        for app in apps:
            if "Admin" in app.get("permissions", []) and "SMS" in app.get("permissions", []):
                app["is_suspicious"] = True
                
        return apps

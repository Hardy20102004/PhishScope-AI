import re
from typing import Dict, Any, List

class IOCExtractionEngine:
    """
    Extracts URLs, Domains, and search keywords from browsing history and downloads.
    """
    
    @staticmethod
    def extract(history: List[Dict[str, Any]], downloads: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        iocs = []
        
        for h in history:
            iocs.append({
                "ioc_type": "url",
                "ioc_value": h.get("url"),
                "source_context": "Browser History"
            })
            if h.get("is_search") and h.get("search_keyword"):
                iocs.append({
                    "ioc_type": "search_keyword",
                    "ioc_value": h.get("search_keyword"),
                    "source_context": "Search Engine Query"
                })
                
        for d in downloads:
            iocs.append({
                "ioc_type": "url",
                "ioc_value": d.get("source_url"),
                "source_context": "File Download Source"
            })
            
        # Deduplicate
        unique_iocs = []
        seen = set()
        for ioc in iocs:
            val = ioc["ioc_value"]
            if val and val not in seen:
                seen.add(val)
                unique_iocs.append(ioc)
                
        return unique_iocs

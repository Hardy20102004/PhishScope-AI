from typing import Any, Dict, List


class TimelineEngine:
    """
    Builds a unified chronological timeline from different artifact sources.
    """
    
    @staticmethod
    def build(history: List[Dict[str, Any]], cookies: List[Dict[str, Any]], downloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        events = []
        
        for h in history:
            events.append({
                "timestamp": h.get("visit_time"),
                "event_type": "Search" if h.get("is_search") else "Visit",
                "description": f"Visited: {h.get('title', h.get('url'))}",
                "source": "History"
            })
            
        for c in cookies:
            events.append({
                "timestamp": c.get("creation_time"),
                "event_type": "CookieCreated",
                "description": f"Cookie {c.get('name')} set by {c.get('domain')}",
                "source": "Cookies"
            })
            
        for d in downloads:
            events.append({
                "timestamp": d.get("download_time"),
                "event_type": "Download",
                "description": f"Downloaded {d.get('filename')} from {d.get('source_url')}",
                "source": "Downloads"
            })
            
        events.sort(key=lambda x: x.get("timestamp", ""))
        return events

from typing import Any, Dict, List


class TimelineEngine:
    """
    Builds a unified chronological timeline from different artifact sources.
    """
    
    @staticmethod
    def build(communications: List[Dict[str, Any]], locations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        events = []
        
        for comm in communications:
            events.append({
                "timestamp": comm.get("timestamp"),
                "event_type": comm.get("comm_type"),
                "description": f"{comm.get('direction')} to/from {comm.get('contact_number')}: {comm.get('body', '')[:50]}...",
                "source": "Communications"
            })
            
        for loc in locations:
            events.append({
                "timestamp": loc.get("timestamp"),
                "event_type": "LocationUpdate",
                "description": f"Location: {loc.get('latitude')}, {loc.get('longitude')} ({loc.get('label', 'Unknown')})",
                "source": loc.get("source", "LocationData")
            })
            
        # Sort by timestamp chronologically
        events.sort(key=lambda x: x.get("timestamp", ""))
        
        return events

from typing import Dict, Any, List

class TimelineEngine:
    @staticmethod
    def build(assets: List[Dict[str, Any]], identities: List[Dict[str, Any]], configs: List[Dict[str, Any]], audits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        events = []
        
        # In a real system, assets/identities might have creation timestamps
        # We'll map the audit logs to build the timeline
        for a in audits:
            events.append({
                "timestamp": a.get("timestamp"),
                "event_type": "Audit",
                "description": f"Actor {a.get('actor')} performed {a.get('event_name')} via {a.get('event_source')} (IP: {a.get('source_ip')})"
            })
            
        events.sort(key=lambda x: x.get("timestamp", ""))
        return events

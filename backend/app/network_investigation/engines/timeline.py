from typing import Any, Dict, List


class TimelineEngine:
    @staticmethod
    def build(flows: List[Dict[str, Any]], dns: List[Dict[str, Any]], http: List[Dict[str, Any]], tls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        events = []
        
        for f in flows:
            events.append({
                "timestamp": f.get("timestamp"),
                "event_type": "Flow",
                "description": f"Connection {f.get('source_ip')}:{f.get('source_port')} -> {f.get('destination_ip')}:{f.get('destination_port')} ({f.get('protocol')})"
            })
            
        for d in dns:
            events.append({
                "timestamp": d.get("timestamp"),
                "event_type": "DNS",
                "description": f"DNS Query: {d.get('query')} ({d.get('record_type')}) -> {', '.join(d.get('answers', []))}"
            })
            
        for h in http:
            events.append({
                "timestamp": h.get("timestamp"),
                "event_type": "HTTP",
                "description": f"HTTP {h.get('method')} {h.get('host')}{h.get('uri')} [{h.get('status_code')}]"
            })
            
        for t in tls:
            events.append({
                "timestamp": t.get("timestamp"),
                "event_type": "TLS",
                "description": f"TLS {t.get('version')} SNI: {t.get('server_name')}"
            })
            
        events.sort(key=lambda x: x.get("timestamp", ""))
        return events

class TimelineBuilder:
    """
    Merges audit logs, container events, and K8s changes into a single chronological view.
    """
    def generate_timeline(self, audit_logs: list) -> list[dict]:
        events = []
        
        for log in audit_logs:
            events.append({
                "timestamp": log.timestamp,
                "type": "AUDIT_LOG",
                "summary": f"{log.actor_identity} called {log.event_name}",
                "is_anomalous": log.is_anomalous
            })
            
        events.sort(key=lambda x: x["timestamp"])
        return events

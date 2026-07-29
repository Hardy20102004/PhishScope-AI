class TimelineBuilder:
    """
    Merges history, downloads, and extension installations into a chronological browser timeline.
    """
    def generate_timeline(self, history: list, extensions: list) -> list[dict]:
        events = []
        
        for h in history:
            events.append({
                "timestamp": h.timestamp,
                "type": "PAGE_VISIT",
                "summary": f"Visited {h.title or h.url}",
                "is_threat": h.is_threat_hit
            })
            
        for e in extensions:
            if e.install_time:
                events.append({
                    "timestamp": e.install_time,
                    "type": "EXTENSION_INSTALL",
                    "summary": f"Installed Extension: {e.name} v{e.version}",
                    "is_threat": e.is_suspicious
                })
            
        # Sort chronologically
        events.sort(key=lambda x: x["timestamp"])
        return events

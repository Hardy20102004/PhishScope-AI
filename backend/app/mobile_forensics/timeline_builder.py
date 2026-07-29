class TimelineBuilder:
    """
    Merges messages, media, and locations into a unified chronological mobile timeline.
    """
    def generate_timeline(self, communications: list, locations: list) -> list[dict]:
        events = []
        
        for c in communications:
            events.append({
                "timestamp": c.timestamp,
                "type": "MESSAGE",
                "source": c.app_name,
                "summary": f"{'Outgoing' if c.is_outgoing else 'Incoming'} message to {c.receiver if c.is_outgoing else c.sender}: '{c.body}'"
            })
            
        for loc in locations:
            events.append({
                "timestamp": loc.timestamp,
                "type": "LOCATION",
                "source": loc.source,
                "summary": f"Device located at {loc.latitude}, {loc.longitude} (Accuracy: {loc.accuracy_meters}m)"
            })
            
        # Sort chronologically
        events.sort(key=lambda x: x["timestamp"])
        return events

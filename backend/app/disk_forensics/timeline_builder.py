from datetime import datetime, timedelta, timezone

class TimelineBuilder:
    """
    Synthesizes MAC (Modified, Accessed, Created) timestamps into a unified forensic timeline.
    """
    def generate_timeline(self) -> list[dict]:
        """
        Simulates sorting file system activity chronologically.
        """
        now = datetime.now(timezone.utc)
        return [
            {"timestamp": now - timedelta(days=2), "event_type": "CREATED", "artifact": "C:\\Temp\\malware.exe"},
            {"timestamp": now - timedelta(days=2, hours=-1), "event_type": "MODIFIED", "artifact": "C:\\Windows\\System32\\cmd.exe"},
            {"timestamp": now - timedelta(days=1), "event_type": "DELETED", "artifact": "[UNALLOCATED]\\carved_file_001.pdf"},
        ]

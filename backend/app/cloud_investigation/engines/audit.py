from typing import Any, Dict, List


class AuditLogAnalysisEngine:
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        logs = parsed_data.get("audit_logs", [])
        anomalous_events = ["StopLogging", "DeleteTrail", "DeleteBucket", "CreateAccessKey"]
        
        for log in logs:
            if not log.get("is_anomalous") and log.get("event_name") in anomalous_events:
                log["is_anomalous"] = True
                
        return logs

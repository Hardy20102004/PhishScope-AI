from typing import Any, Dict, List


class HTTPAnalysisEngine:
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        http_logs = parsed_data.get("http", [])
        http_records = []
        for h in http_logs:
            http_records.append({
                "timestamp": h.get("ts"),
                "method": h.get("method"),
                "host": h.get("host"),
                "uri": h.get("uri"),
                "status_code": h.get("status_code"),
                "user_agent": h.get("user_agent")
            })
        return http_records

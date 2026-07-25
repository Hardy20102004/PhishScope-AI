from typing import Dict, Any, List

class FlowAnalysisEngine:
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        conn_logs = parsed_data.get("conn", [])
        flows = []
        for c in conn_logs:
            flows.append({
                "timestamp": c.get("ts"),
                "source_ip": c.get("id.orig_h"),
                "destination_ip": c.get("id.resp_h"),
                "source_port": c.get("id.orig_p"),
                "destination_port": c.get("id.resp_p"),
                "protocol": c.get("proto"),
                "bytes_sent": c.get("orig_bytes", 0),
                "bytes_received": c.get("resp_bytes", 0),
                "duration": c.get("duration", 0.0)
            })
        return flows

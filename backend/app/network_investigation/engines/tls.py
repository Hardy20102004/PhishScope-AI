from typing import Any, Dict, List


class TLSAnalysisEngine:
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        tls_logs = parsed_data.get("tls", [])
        tls_records = []
        for t in tls_logs:
            tls_records.append({
                "timestamp": t.get("ts"),
                "server_name": t.get("server_name"),
                "version": t.get("version"),
                "cipher": t.get("cipher"),
                "ja3_fingerprint": t.get("ja3")
            })
        return tls_records

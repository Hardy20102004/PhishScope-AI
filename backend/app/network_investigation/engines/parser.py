import json
from typing import Dict, Any

class PCAPProcessingEngine:
    """
    Simulates parsing Zeek/PCAP json output into structured logs.
    """
    
    @staticmethod
    def parse(payload: str) -> Dict[str, Any]:
        try:
            data = json.loads(payload)
            return data
        except:
            # Fallback mock for testing
            return {
                "conn": [
                    {"ts": "2024-01-01T10:00:00Z", "id.orig_h": "192.168.1.10", "id.resp_h": "8.8.8.8", "id.orig_p": 54321, "id.resp_p": 53, "proto": "udp", "orig_bytes": 45, "resp_bytes": 100, "duration": 0.05},
                    {"ts": "2024-01-01T10:00:05Z", "id.orig_h": "192.168.1.10", "id.resp_h": "104.21.3.44", "id.orig_p": 54322, "id.resp_p": 443, "proto": "tcp", "orig_bytes": 1500, "resp_bytes": 5000, "duration": 1.2}
                ],
                "dns": [
                    {"ts": "2024-01-01T10:00:00Z", "query": "api.malicious-c2-domain.com", "qtype_name": "A", "rcode_name": "NOERROR", "answers": ["104.21.3.44"]}
                ],
                "http": [
                    {"ts": "2024-01-01T10:01:00Z", "method": "POST", "host": "api.malicious-c2-domain.com", "uri": "/beacon", "status_code": 200, "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                ],
                "tls": [
                    {"ts": "2024-01-01T10:00:05Z", "server_name": "api.malicious-c2-domain.com", "version": "TLSv1.3", "cipher": "TLS_AES_256_GCM_SHA384", "ja3": "d41d8cd98f00b204e9800998ecf8427e"}
                ]
            }

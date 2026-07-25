import re
from typing import Dict, Any, List

class IOCExtractionEngine:
    @staticmethod
    def extract(dns: List[Dict[str, Any]], http: List[Dict[str, Any]], tls: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        iocs = []
        
        for d in dns:
            iocs.append({
                "ioc_type": "domain",
                "ioc_value": d.get("query"),
                "source_context": "DNS Query"
            })
            for ans in d.get("answers", []):
                iocs.append({
                    "ioc_type": "ip" if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ans) else "domain",
                    "ioc_value": ans,
                    "source_context": "DNS Answer"
                })
                
        for h in http:
            iocs.append({
                "ioc_type": "domain",
                "ioc_value": h.get("host"),
                "source_context": "HTTP Host Header"
            })
            iocs.append({
                "ioc_type": "url",
                "ioc_value": f"http://{h.get('host')}{h.get('uri')}",
                "source_context": "HTTP Request"
            })
            
        for t in tls:
            if t.get("server_name"):
                iocs.append({
                    "ioc_type": "domain",
                    "ioc_value": t.get("server_name"),
                    "source_context": "TLS SNI"
                })
                
        # Deduplicate
        unique_iocs = []
        seen = set()
        for ioc in iocs:
            val = ioc["ioc_value"]
            if val and val not in seen:
                seen.add(val)
                unique_iocs.append(ioc)
                
        return unique_iocs

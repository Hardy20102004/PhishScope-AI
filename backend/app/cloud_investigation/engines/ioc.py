import re
from typing import Dict, Any, List

class IOCExtractionEngine:
    @staticmethod
    def extract(audits: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        iocs = []
        
        for a in audits:
            ip = a.get("source_ip")
            if ip and re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
                iocs.append({
                    "ioc_type": "ip",
                    "ioc_value": ip,
                    "source_context": f"Audit Log: {a.get('event_name')}"
                })
            actor = a.get("actor")
            if actor:
                iocs.append({
                    "ioc_type": "cloud_id",
                    "ioc_value": actor,
                    "source_context": f"Audit Log Actor"
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

import re
from typing import Dict, Any, List

class IOCExtractionEngine:
    """
    Extracts URLs, IPs, and Phone numbers from communications.
    """
    
    @staticmethod
    def extract(communications: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        iocs = []
        
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        
        for comm in communications:
            # Extract URLs from SMS bodies
            body = comm.get("body", "")
            if body:
                urls = re.findall(url_pattern, body)
                for u in urls:
                    iocs.append({
                        "ioc_type": "url",
                        "ioc_value": u,
                        "source_context": f"SMS {comm.get('direction')} to/from {comm.get('contact_number')}"
                    })
                    
            # The contact number itself is an IOC
            number = comm.get("contact_number")
            if number:
                iocs.append({
                    "ioc_type": "phone_number",
                    "ioc_value": number,
                    "source_context": f"Communication Log ({comm.get('comm_type')})"
                })
                
        # Deduplicate
        unique_iocs = []
        seen = set()
        for ioc in iocs:
            val = ioc["ioc_value"]
            if val not in seen:
                seen.add(val)
                unique_iocs.append(ioc)
                
        return unique_iocs

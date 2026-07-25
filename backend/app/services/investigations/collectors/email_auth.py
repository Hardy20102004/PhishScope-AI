from typing import Dict, Any
from app.services.investigations.collectors.base import BaseCollector

class EmailAuthCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        """
        Takes the `Authentication-Results` header string as target,
        and parses out SPF, DKIM, and DMARC status.
        """
        evidence = {
            "spf": "unknown",
            "dkim": "unknown",
            "dmarc": "unknown",
            "raw_header": target
        }
        
        if not target:
            return evidence
            
        target_lower = target.lower()
        
        # Extremely basic parsing of the Authentication-Results header.
        # Real-world auth headers look like:
        # "mx.google.com; dkim=pass header.i=@domain.com; spf=pass (google.com: domain designates IP as permitted sender) smtp.mailfrom=domain.com; dmarc=pass"
        
        # SPF
        if "spf=pass" in target_lower:
            evidence["spf"] = "pass"
        elif "spf=fail" in target_lower or "spf=softfail" in target_lower:
            evidence["spf"] = "fail"
            
        # DKIM
        if "dkim=pass" in target_lower:
            evidence["dkim"] = "pass"
        elif "dkim=fail" in target_lower:
            evidence["dkim"] = "fail"
            
        # DMARC
        if "dmarc=pass" in target_lower or "dmarc=bestguesspass" in target_lower:
            evidence["dmarc"] = "pass"
        elif "dmarc=fail" in target_lower:
            evidence["dmarc"] = "fail"
            
        return evidence

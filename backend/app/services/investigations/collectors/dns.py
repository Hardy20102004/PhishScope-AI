import dns.resolver
from typing import Dict, Any
from urllib.parse import urlparse
from app.services.investigations.collectors.base import BaseCollector

class DNSCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        evidence = {}
        
        # Parse hostname from target
        parsed = urlparse(target)
        hostname = parsed.hostname if parsed.hostname else target
        
        # Remove port if present
        if ":" in hostname:
            hostname = hostname.split(":")[0]
            
        record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS']
        
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(hostname, rtype, lifetime=2.0)
                evidence[rtype] = [str(rdata) for rdata in answers]
            except dns.resolver.NoAnswer:
                evidence[rtype] = []
            except dns.resolver.NXDOMAIN:
                return {"error": "Domain does not exist (NXDOMAIN)"}
            except Exception as e:
                evidence[rtype] = f"Error: {str(e)}"
                
        return evidence

import re
import ipaddress
from urllib.parse import urlparse
import hashlib

from app.models.threat_intel import IOCType

class NormalizationEngine:
    @staticmethod
    def normalize(ioc_value: str, ioc_type: IOCType) -> tuple[str, dict]:
        """
        Normalizes an IOC based on its type.
        Returns a tuple of (canonical_value, metadata).
        """
        metadata = {"original_value": ioc_value}
        
        # Remove common defanging techniques
        ioc_value = NormalizationEngine.undefang(ioc_value)
        if ioc_value != metadata["original_value"]:
            metadata["defanged"] = True
            
        canonical_value = ioc_value
        
        if ioc_type == IOCType.IPV4 or ioc_type == IOCType.IPV6:
            try:
                canonical_value = str(ipaddress.ip_address(ioc_value))
            except ValueError:
                pass # Return as is if invalid
                
        elif ioc_type == IOCType.DOMAIN or ioc_type == IOCType.SUBDOMAIN:
            canonical_value = ioc_value.lower().strip()
            # Remove trailing dot if present
            if canonical_value.endswith('.'):
                canonical_value = canonical_value[:-1]
                
        elif ioc_type == IOCType.URL:
            # Basic URL canonicalization
            try:
                if not ioc_value.startswith(('http://', 'https://', 'ftp://')):
                    parsed = urlparse('http://' + ioc_value)
                else:
                    parsed = urlparse(ioc_value)
                
                # Lowercase scheme and netloc
                canonical_value = f"{parsed.scheme}://{parsed.netloc.lower()}{parsed.path}"
                if parsed.query:
                    # Sort query parameters for consistency
                    queries = parsed.query.split('&')
                    queries.sort()
                    canonical_value += f"?{'&'.join(queries)}"
            except Exception:
                pass  # intentionally silenced - non-critical enrichment failure
                
        elif ioc_type == IOCType.EMAIL:
            canonical_value = ioc_value.lower().strip()
            
        elif ioc_type in (IOCType.SHA256, IOCType.SHA1, IOCType.MD5, IOCType.JA3, IOCType.JA4):
            canonical_value = ioc_value.lower().strip()
            
        elif ioc_type == IOCType.PHONE:
            # Strip everything except digits and plus sign
            canonical_value = re.sub(r'[^\d+]', '', ioc_value)
            
        return canonical_value, metadata

    @staticmethod
    def undefang(value: str) -> str:
        """
        Removes common defanging like hxxp, [.]
        """
        value = value.replace('[.]', '.')
        value = value.replace('(', '.')
        value = value.replace(')', '.')
        value = value.replace('{.}', '.')
        
        if value.lower().startswith('hxxp://'):
            value = 'http://' + value[7:]
        elif value.lower().startswith('hxxps://'):
            value = 'https://' + value[8:]
            
        return value

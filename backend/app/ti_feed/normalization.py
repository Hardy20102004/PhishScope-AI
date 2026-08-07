import re
from typing import Dict, Any, Tuple
from app.models.threat_intel import IOCType

class FeedNormalizer:
    """
    Translates external format indicators into PHOENIX internal IOCType format.
    The actual canonicalization (lowercasing, undefanging) is deferred to the IOC Engine.
    """

    @staticmethod
    def normalize_to_internal(data: Dict[str, Any]) -> Tuple[str, IOCType]:
        """
        Returns (extracted_value, internal_ioc_type).
        """
        raw_val = str(data.get("value", ""))
        raw_type = str(data.get("type", "")).lower()

        extracted_value = raw_val
        internal_type = IOCType.CUSTOM

        # 1. Parse STIX Patterns
        if raw_type == "stix pattern" or raw_val.startswith("["):
            extracted_value, internal_type = FeedNormalizer._parse_stix_pattern(raw_val)
        
        # 2. Map standard types (e.g., from MISP or CSVs)
        elif raw_type in ["ip", "ip-src", "ip-dst", "ipv4"]:
            internal_type = IOCType.IPV4
        elif raw_type in ["domain", "hostname"]:
            internal_type = IOCType.DOMAIN
        elif raw_type in ["url", "uri"]:
            internal_type = IOCType.URL
        elif raw_type in ["email-src", "email-dst", "email"]:
            internal_type = IOCType.EMAIL
        elif raw_type == "sha256":
            internal_type = IOCType.SHA256
        elif raw_type == "md5":
            internal_type = IOCType.MD5

        return extracted_value, internal_type

    @staticmethod
    def _parse_stix_pattern(pattern: str) -> Tuple[str, IOCType]:
        """
        Very basic STIX 2.1 Pattern parser for extraction.
        E.g., [ipv4-addr:value = '198.51.100.1/32'] -> '198.51.100.1/32', IPV4
        """
        # Match something like [type:property = 'value']
        match = re.search(r"\[\s*([\w\-]+):[^=]+=\s*'([^']+)'\s*\]", pattern)
        if match:
            obj_type = match.group(1)
            value = match.group(2)
            
            mapping = {
                "ipv4-addr": IOCType.IPV4,
                "ipv6-addr": IOCType.IPV6,
                "domain-name": IOCType.DOMAIN,
                "url": IOCType.URL,
                "email-addr": IOCType.EMAIL,
                "file": IOCType.FILE_NAME, # Could also be hash if property was file:hashes.'SHA-256'
            }
            return value, mapping.get(obj_type, IOCType.CUSTOM)
            
        return pattern, IOCType.CUSTOM

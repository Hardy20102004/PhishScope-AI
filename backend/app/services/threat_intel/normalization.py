import ipaddress
import re
from urllib.parse import urlparse


class IndicatorNormalizationEngine:
    """Normalizes and categorizes indicators."""

    @staticmethod
    def identify_type(value: str) -> str:
        """Identify the type of the indicator."""
        value = value.strip()
        
        # Check IPv4/IPv6
        try:
            ip = ipaddress.ip_address(value)
            return f"ipv{ip.version}"
        except ValueError:
            pass
            
        # Check MD5/SHA1/SHA256
        if re.match(r'^[a-fA-F0-9]{32}$', value):
            return "md5"
        if re.match(r'^[a-fA-F0-9]{40}$', value):
            return "sha1"
        if re.match(r'^[a-fA-F0-9]{64}$', value):
            return "sha256"
            
        # Check Email
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            return "email"
            
        # Check URL (very basic check)
        if value.startswith('http://') or value.startswith('https://'):
            return "url"
            
        # Default to domain if it looks like one
        if re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', value):
            return "domain"
            
        return "unknown"

    @staticmethod
    def normalize(value: str, indicator_type: str) -> str:
        """Normalize the indicator value for consistent lookup."""
        value = value.strip()
        
        if indicator_type in ("md5", "sha1", "sha256"):
            return value.lower()
            
        if indicator_type == "email":
            return value.lower()
            
        if indicator_type == "url":
            # Very basic normalization, could be expanded (e.g. drop fragments, standardize query params)
            parsed = urlparse(value)
            scheme = parsed.scheme.lower()
            netloc = parsed.netloc.lower()
            # simple rebuild
            return f"{scheme}://{netloc}{parsed.path}"
            
        if indicator_type == "domain":
            return value.lower()
            
        return value

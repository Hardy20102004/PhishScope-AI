import ipaddress
import socket
from urllib.parse import urlparse


class SSRFError(Exception):
    pass

class SSRFValidator:
    """
    Validates that a URL does not resolve to an internal or reserved IP address
    to prevent Server-Side Request Forgery (SSRF) attacks.
    """
    
    @staticmethod
    def is_safe_url(url: str) -> bool:
        try:
            url = url.strip()
            parsed = urlparse(url)
            hostname = parsed.hostname.strip() if parsed.hostname else None
            
            if not hostname:
                raise SSRFError("Invalid URL structure.")
                
            # Resolve DNS
            # Note: In a true async environment, we should use an async DNS resolver like aiodns,
            # but socket.gethostbyname is synchronous.
            ip_str = socket.gethostbyname(hostname)
            ip = ipaddress.ip_address(ip_str)
            
            # Check if IP is private, loopback, or reserved
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast:
                raise SSRFError(f"URL resolves to an internal/reserved IP ({ip_str})")
                
            return True
            
        except socket.gaierror as e:
            # If DNS fails to resolve, it might be an invalid domain or temporary network issue.
            # We allow it to pass SSRF validation; httpx will naturally fail to connect later,
            # which is handled gracefully by the engine's collect_evidence() phase.
            return True
        except Exception as e:
            raise SSRFError(f"SSRF Validation failed: {str(e)}")

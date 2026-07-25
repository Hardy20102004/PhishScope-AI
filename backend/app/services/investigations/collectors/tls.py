import ssl
import socket
from typing import Dict, Any
from urllib.parse import urlparse
from datetime import datetime
from app.services.investigations.collectors.base import BaseCollector

class TLSCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        # Only collect TLS if it's HTTPS
        if not target.startswith("https://"):
            return {"error": "Not an HTTPS target"}
            
        parsed = urlparse(target)
        hostname = parsed.hostname
        port = parsed.port or 443
        
        if not hostname:
            return {"error": "Invalid hostname for TLS"}
            
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        try:
            with socket.create_connection((hostname, port), timeout=3.0) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert(binary_form=False)
                    # When CERT_NONE is used, getpeercert() returns empty dict.
                    # We must briefly reconnect with verification to get the dict, 
                    # but we catch errors if the cert is invalid so we can still report it.
                    pass
        except Exception as e:
            pass # fallback to trying to get cert details anyway
            
        try:
             # Get actual cert dict
             context_verify = ssl.create_default_context()
             with socket.create_connection((hostname, port), timeout=3.0) as sock:
                with context_verify.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        "issuer": dict(x[0] for x in cert.get("issuer", [])),
                        "subject": dict(x[0] for x in cert.get("subject", [])),
                        "notBefore": cert.get("notBefore"),
                        "notAfter": cert.get("notAfter"),
                        "subjectAltName": [x[1] for x in cert.get("subjectAltName", [])],
                        "version": ssock.version(),
                        "cipher": ssock.cipher(),
                        "valid": True
                    }
        except ssl.SSLCertVerificationError as e:
            return {"error": "Certificate Verification Failed", "details": str(e), "valid": False}
        except Exception as e:
            return {"error": str(e), "valid": False}

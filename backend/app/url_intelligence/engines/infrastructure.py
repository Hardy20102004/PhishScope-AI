import dns.resolver
import socket
import ssl
from datetime import datetime, timezone
import json

class InfrastructureCorrelationEngine:
    """
    Collects Domain Intelligence, Infrastructure Correlation, and Certificate Analysis.
    """
    
    @staticmethod
    async def analyze(domain: str) -> dict:
        if not domain:
            return {}
            
        infrastructure = {
            "domain_name": domain,
            "ips": [],
            "nameservers": [],
            "mx_records": [],
            "txt_records": [],
            "certificates": []
        }
        
        # DNS Resolution (Synchronous for now, could use aio-dns for full async)
        try:
            answers = dns.resolver.resolve(domain, 'A')
            infrastructure["ips"] = [rdata.address for rdata in answers]
        except Exception:
            pass
            
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            infrastructure["nameservers"] = [rdata.to_text() for rdata in answers]
        except Exception:
            pass
            
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            infrastructure["mx_records"] = [rdata.to_text() for rdata in answers]
        except Exception:
            pass
            
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            infrastructure["txt_records"] = [rdata.to_text() for rdata in answers]
        except Exception:
            pass
            
        # Certificate Analysis
        try:
            cert_data = InfrastructureCorrelationEngine.get_certificate(domain)
            if cert_data:
                infrastructure["certificates"].append(cert_data)
        except Exception as e:
            pass
            
        return infrastructure

    @staticmethod
    def get_certificate(hostname: str, port: int = 443) -> dict:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE # We want to inspect even invalid certs
        
        try:
            with socket.create_connection((hostname, port), timeout=3.0) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert(binary_form=False) # This gives decoded dict if verify_mode was CERT_REQUIRED, but since CERT_NONE it might be empty.
                    # Actually, getpeercert() with CERT_NONE returns empty dict. Let's use CERT_REQUIRED to get details, or parse binary.
                    pass
        except Exception:
            pass
            
        # Refined certificate fetching for details
        context = ssl.create_default_context()
        try:
            with socket.create_connection((hostname, port), timeout=3.0) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse basic cert details
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    subject = dict(x[0] for x in cert.get('subject', []))
                    
                    return {
                        "issuer": issuer.get('commonName', str(issuer)),
                        "subject": subject.get('commonName', str(subject)),
                        "valid_from": cert.get('notBefore'),
                        "valid_to": cert.get('notAfter'),
                        "subject_alt_names": [x[1] for x in cert.get('subjectAltName', [])],
                        "tls_version": ssock.version(),
                        "is_valid": True
                    }
        except ssl.SSLError as e:
            return {
                "issuer": "Unknown",
                "subject": "Unknown",
                "is_valid": False,
                "error": str(e)
            }
        except Exception:
            return None

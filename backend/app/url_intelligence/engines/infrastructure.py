import asyncio
import socket
import ssl
import logging
from typing import Optional

import dns.resolver


logger = logging.getLogger(__name__)


class InfrastructureCorrelationEngine:
    """
    Collects Domain Intelligence, Infrastructure Correlation, and Certificate Analysis.
    
    Fixes applied (v2):
    - BUG-001: Removed dead first SSL context block (was connecting and doing nothing for 3s)
    - BUG-001: DNS resolver calls now run in asyncio.to_thread() to avoid blocking the event loop
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
        
        # DNS Resolution — using asyncio.to_thread to avoid blocking the event loop
        # (dns.resolver is synchronous; this is the correct pattern for async FastAPI)
        async def resolve(record_type: str) -> list:
            try:
                answers = await asyncio.to_thread(dns.resolver.resolve, domain, record_type)
                if record_type == 'A':
                    return [rdata.address for rdata in answers]
                return [rdata.to_text() for rdata in answers]
            except Exception:
                return []
        
        # Run all DNS lookups in parallel
        ip_task = asyncio.create_task(resolve('A'))
        ns_task = asyncio.create_task(resolve('NS'))
        mx_task = asyncio.create_task(resolve('MX'))
        txt_task = asyncio.create_task(resolve('TXT'))
        
        results = await asyncio.gather(ip_task, ns_task, mx_task, txt_task, return_exceptions=True)
        
        infrastructure["ips"] = results[0] if not isinstance(results[0], Exception) else []
        infrastructure["nameservers"] = results[1] if not isinstance(results[1], Exception) else []
        infrastructure["mx_records"] = results[2] if not isinstance(results[2], Exception) else []
        infrastructure["txt_records"] = results[3] if not isinstance(results[3], Exception) else []
        
        # Certificate Analysis — run in thread to avoid blocking
        try:
            cert_data = await asyncio.to_thread(
                InfrastructureCorrelationEngine.get_certificate, domain
            )
            if cert_data:
                infrastructure["certificates"].append(cert_data)
        except Exception as e:
            logger.debug(f"Certificate fetch failed for {domain}: {e}")
            
        return infrastructure

    @staticmethod
    def get_certificate(hostname: str, port: int = 443) -> Optional[dict]:
        """
        Fetches and parses TLS certificate details from a host.
        
        Fixed: Removed dead first SSL context block that was wasting 3 seconds
        per scan by connecting, wrapping SSL, and doing nothing (pass).
        """
        context = ssl.create_default_context()
        
        try:
            with socket.create_connection((hostname, port), timeout=5.0) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
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
        except ssl.SSLCertVerificationError as e:
            # Certificate exists but is invalid/expired — still collect info
            try:
                ctx_no_verify = ssl.create_default_context()
                ctx_no_verify.check_hostname = False
                ctx_no_verify.verify_mode = ssl.CERT_NONE
                with socket.create_connection((hostname, port), timeout=5.0) as sock:
                    with ctx_no_verify.wrap_socket(sock, server_hostname=hostname) as ssock:
                        # binary_form=True gives DER bytes we can at least note
                        return {
                            "issuer": "Unknown (verification failed)",
                            "subject": hostname,
                            "valid_from": None,
                            "valid_to": None,
                            "subject_alt_names": [],
                            "tls_version": ssock.version(),
                            "is_valid": False,
                            "error": str(e)
                        }
            except Exception:
                return {
                    "issuer": "Unknown",
                    "subject": "Unknown",
                    "is_valid": False,
                    "error": str(e)
                }
        except ssl.SSLError as e:
            return {
                "issuer": "Unknown",
                "subject": "Unknown",
                "is_valid": False,
                "error": str(e)
            }
        except (socket.timeout, ConnectionRefusedError, OSError):
            # Host not reachable on port 443 — not necessarily malicious
            return None
        except Exception as e:
            logger.debug(f"Unexpected cert error for {hostname}: {e}")
            return None

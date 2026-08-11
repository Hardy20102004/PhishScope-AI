import re
from urllib.parse import urlparse

import httpx

from app.schemas.investigation import Finding
from app.services.investigations.pipeline import BaseInvestigationEngine
from app.services.investigations.validators import SSRFError, SSRFValidator


class URLEngine(BaseInvestigationEngine):
    
    def validate(self) -> bool:
        try:
            # Ensure it has a scheme
            self.target = self.target.strip()
            if not self.target.startswith(("http://", "https://")):
                self.target = "http://" + self.target
                
            SSRFValidator.is_safe_url(self.target)
            return True
        except SSRFError as e:
            self.error_message = str(e)
            return False
            
    def collect_evidence(self) -> None:
        """Fetch HTTP headers, status code, and redirect chains."""
        import dns.resolver
        import ssl
        import socket
        from bs4 import BeautifulSoup

        parsed = urlparse(self.target)
        hostname = parsed.hostname or ""

        # --- HTTP & Content Evidence ---
        html_content = ""
        try:
            # Use httpx for the request. Disable SSL verify for scanning purposes to catch bad certs later
            with httpx.Client(verify=False, timeout=5.0, follow_redirects=True) as client:
                response = client.get(self.target)
                html_content = response.text
                
                # Extract Redirect Chain
                redirects = []
                for r in response.history:
                    redirects.append({
                        "url": str(r.url),
                        "status_code": r.status_code
                    })
                redirects.append({
                    "url": str(response.url),
                    "status_code": response.status_code
                })
                
                self.evidence = {
                    "http": {
                        "final_url": str(response.url),
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "redirect_chain": redirects,
                        "server": response.headers.get("server", "Unknown"),
                    }
                }
        except httpx.RequestError as e:
            self.evidence = {"http": {"connection_error": str(e)}}

        # --- Content Evidence ---
        if html_content:
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.title.string if soup.title else ""
                forms = soup.find_all('form')
                hidden = soup.find_all(type='hidden')
                scripts = soup.find_all('script')
                
                text_content = soup.get_text().lower()
                suspicious_keywords = ["login", "verify", "account", "update", "secure", "banking", "wallet", "support"]
                found_keywords = list(set([kw for kw in suspicious_keywords if kw in text_content]))
                
                self.evidence["content"] = {
                    "title": title.strip() if title else "",
                    "forms_count": len(forms),
                    "hidden_elements": len(hidden),
                    "scripts_count": len(scripts),
                    "suspicious_keywords_found": found_keywords
                }
            except Exception as e:
                self.evidence["content"] = {"error": str(e)}

        # --- DNS Evidence ---
        if hostname:
            dns_records = {}
            for rtype in ['A', 'AAAA', 'MX', 'TXT', 'NS']:
                try:
                    answers = dns.resolver.resolve(hostname, rtype, lifetime=2.0)
                    dns_records[rtype] = [str(rdata) for rdata in answers]
                except Exception:
                    pass
            self.evidence["dns"] = dns_records if dns_records else {"error": "No records found or domain resolution failed"}

        # --- TLS Evidence ---
        if hostname and self.target.startswith("https://"):
            try:
                from cryptography import x509
                from cryptography.hazmat.backends import default_backend
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with socket.create_connection((hostname, 443), timeout=5.0) as sock:
                    with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                        der_cert = ssock.getpeercert(binary_form=True)
                        
                        cert = x509.load_der_x509_certificate(der_cert, default_backend())
                        
                        issuer_cn = ""
                        issuer_o = ""
                        for attr in cert.issuer:
                            if attr.oid == x509.NameOID.COMMON_NAME:
                                issuer_cn = attr.value
                            elif attr.oid == x509.NameOID.ORGANIZATION_NAME:
                                issuer_o = attr.value
                                
                        subject_cn = ""
                        for attr in cert.subject:
                            if attr.oid == x509.NameOID.COMMON_NAME:
                                subject_cn = attr.value
                                
                        sans = []
                        try:
                            ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
                            for name in ext.value:
                                if hasattr(name, 'value'):
                                    sans.append(name.value)
                        except x509.ExtensionNotFound:
                            pass
                            
                        not_after = str(cert.not_valid_after_utc) if hasattr(cert, 'not_valid_after_utc') else str(cert.not_valid_after)
                                
                        self.evidence["tls"] = {
                            "valid": True,
                            "issuer": {
                                "organizationName": issuer_o,
                                "commonName": issuer_cn
                            },
                            "subject": {
                                "commonName": subject_cn
                            },
                            "notAfter": not_after,
                            "subjectAltName": sans,
                            "version": ssock.version(),
                            "cipher": ssock.cipher()
                        }
            except Exception as e:
                self.evidence["tls"] = {"error": str(e), "valid": False}
            
    def analyze(self) -> None:
        """Run URL heuristics against the target and collected evidence."""
        parsed = urlparse(self.target)
        hostname = parsed.hostname or ""
        
        # 1. Suspicious Keywords (Phishing)
        suspicious_keywords = ["login", "verify", "account", "update", "secure", "banking", "wallet", "support"]
        for keyword in suspicious_keywords:
            if keyword in hostname.lower():
                self.findings.append(Finding(
                    title="Suspicious Keyword in Domain",
                    description=f"The domain contains the high-risk keyword: '{keyword}'",
                    severity="HIGH"
                ))
                
        # 2. IP Address as Hostname
        # Simple regex to check if hostname is just an IPv4
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", hostname):
            self.findings.append(Finding(
                title="IP Address Hostname",
                description="The URL uses an IP address instead of a domain name.",
                severity="MEDIUM"
            ))
            
        # 3. Deep Subdomain depth
        subdomains = hostname.split(".")
        if len(subdomains) > 4:
            self.findings.append(Finding(
                title="Deep Subdomain Depth",
                description=f"The domain uses an unusually high number of subdomains ({len(subdomains)}).",
                severity="MEDIUM"
            ))
            
        # 4. Redirect Analysis
        http_ev = self.evidence.get("http", {})
        redirects = http_ev.get("redirect_chain", [])
        if len(redirects) > 2:
             self.findings.append(Finding(
                title="Multiple Redirects",
                description=f"The URL redirects {len(redirects)-1} times before reaching the final destination.",
                severity="LOW"
            ))
             
        # 5. Connection failures
        if "connection_error" in http_ev:
             self.findings.append(Finding(
                title="Connection Failed",
                description="The engine was unable to establish an HTTP connection to the target.",
                severity="LOW"
            ))

    def score(self) -> None:
        """Calculate score based on findings severity."""
        base_score = 0
        
        weights = {
            "CRITICAL": 50,
            "HIGH": 30,
            "MEDIUM": 15,
            "LOW": 5
        }
        
        for finding in self.findings:
            base_score += weights.get(finding.severity, 0)
            
        # Cap at 100
        self.risk_score = min(base_score, 100)
        
        if self.risk_score >= 70:
            self.risk_level = "CRITICAL"
        elif self.risk_score >= 40:
            self.risk_level = "HIGH"
        elif self.risk_score >= 15:
            self.risk_level = "MEDIUM"
        else:
            self.risk_level = "LOW"

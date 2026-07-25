import concurrent.futures
from urllib.parse import urlparse
from app.services.investigations.pipeline import BaseInvestigationEngine
from app.services.investigations.validators import SSRFValidator, SSRFError
from app.schemas.investigation import Finding
from app.services.investigations.collectors.dns import DNSCollector
from app.services.investigations.collectors.tls import TLSCollector
from app.services.investigations.collectors.http import HTTPCollector
from app.services.investigations.collectors.content import ContentCollector

class WebsiteEngine(BaseInvestigationEngine):
    
    def validate(self) -> bool:
        try:
            if not self.target.startswith(("http://", "https://")):
                self.target = "https://" + self.target
                
            SSRFValidator.is_safe_url(self.target)
            return True
        except SSRFError as e:
            self.error_message = str(e)
            return False
            
    def collect_evidence(self) -> None:
        """
        Executes the DNS, TLS, and HTTP collectors concurrently using a ThreadPool.
        After HTTP completes, it passes the raw body to the Content collector.
        """
        dns_collector = DNSCollector()
        tls_collector = TLSCollector()
        http_collector = HTTPCollector()
        content_collector = ContentCollector()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_dns = executor.submit(dns_collector.collect, self.target)
            future_tls = executor.submit(tls_collector.collect, self.target)
            future_http = executor.submit(http_collector.collect, self.target)
            
            self.evidence["dns"] = future_dns.result()
            self.evidence["tls"] = future_tls.result()
            self.evidence["http"] = future_http.result()
            
        # Extract raw body from HTTP evidence to pass to Content Collector
        raw_body = self.evidence["http"].get("raw_body", "")
        self.evidence["content"] = content_collector.collect(self.target, html_body=raw_body)
        
        # Remove raw body from evidence to save database space, we just wanted the parsed metadata
        if "raw_body" in self.evidence["http"]:
            del self.evidence["http"]["raw_body"]

    def analyze(self) -> None:
        """Analyze the collected evidence and generate findings."""
        parsed = urlparse(self.target)
        hostname = parsed.hostname or ""
        
        # --- TLS Analysis ---
        tls_ev = self.evidence.get("tls", {})
        if "error" in tls_ev:
             self.findings.append(Finding(
                title="TLS Certificate Error",
                description=f"TLS handshake failed: {tls_ev['error']}",
                severity="MEDIUM"
            ))
        elif not tls_ev.get("valid", False):
            self.findings.append(Finding(
                title="Invalid TLS Certificate",
                description="The TLS certificate is untrusted or self-signed.",
                severity="HIGH"
            ))
            
        # --- Content Analysis ---
        content_ev = self.evidence.get("content", {})
        if content_ev.get("hidden_elements", 0) > 2:
             self.findings.append(Finding(
                title="Hidden Elements Detected",
                description=f"The page contains {content_ev['hidden_elements']} hidden input elements, often used for data exfiltration.",
                severity="MEDIUM"
            ))
            
        keywords = content_ev.get("suspicious_keywords_found", [])
        if len(keywords) > 0:
            self.findings.append(Finding(
                title="Suspicious Keywords in Content",
                description=f"The page contains high-risk keywords: {', '.join(keywords)}",
                severity="HIGH"
            ))
            
        # --- HTTP Analysis ---
        http_ev = self.evidence.get("http", {})
        redirects = http_ev.get("redirect_chain", [])
        if len(redirects) > 2:
             self.findings.append(Finding(
                title="Multiple Redirects",
                description=f"The URL redirects {len(redirects)-1} times before reaching the final destination.",
                severity="LOW"
            ))

    def score(self) -> None:
        """Calculate the risk score."""
        base_score = 0
        weights = {"CRITICAL": 50, "HIGH": 30, "MEDIUM": 15, "LOW": 5}
        
        for finding in self.findings:
            base_score += weights.get(finding.severity, 0)
            
        self.risk_score = min(base_score, 100)
        
        if self.risk_score >= 70:
            self.risk_level = "CRITICAL"
        elif self.risk_score >= 40:
            self.risk_level = "HIGH"
        elif self.risk_score >= 15:
            self.risk_level = "MEDIUM"
        else:
            self.risk_level = "LOW"

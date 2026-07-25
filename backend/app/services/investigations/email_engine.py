from typing import Optional

from bs4 import BeautifulSoup

from app.schemas.investigation import Finding
from app.services.investigations.collectors.email_auth import EmailAuthCollector
from app.services.investigations.collectors.email_parser import EmailParserCollector
from app.services.investigations.pipeline import BaseInvestigationEngine


class EmailEngine(BaseInvestigationEngine):
    
    def __init__(self, target: str, raw_content: Optional[str] = None):
        super().__init__(target)
        self.raw_content = raw_content
    
    def validate(self) -> bool:
        if not self.raw_content:
            self.error_message = "No raw .eml content provided."
            return False
        return True
            
    def collect_evidence(self) -> None:
        """
        Parses the raw email content.
        """
        parser = EmailParserCollector()
        auth = EmailAuthCollector()
        
        parsed_data = parser.collect(self.raw_content or "")
        
        # Extract auth results from headers
        auth_header = ""
        if "Authentication-Results" in parsed_data.get("headers", {}):
            # headers is a dict of lists, so we get the first one (or join them)
            auth_header = " ".join(parsed_data["headers"]["Authentication-Results"])
            
        auth_data = auth.collect(auth_header)
        
        # Extract URLs from HTML body
        html = parsed_data.get("body_html", "")
        urls = []
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a', href=True):
                if a['href'].startswith(('http://', 'https://')):
                    urls.append(a['href'])
        
        parsed_data["urls_extracted"] = list(set(urls))
        
        self.evidence["parsed"] = parsed_data
        self.evidence["auth"] = auth_data
        
    def analyze(self) -> None:
        """Analyze the collected evidence and generate findings."""
        parsed = self.evidence.get("parsed", {})
        auth = self.evidence.get("auth", {})
        
        # --- Auth Analysis ---
        if auth.get("spf") == "fail" or auth.get("dkim") == "fail" or auth.get("dmarc") == "fail":
            self.findings.append(Finding(
                title="Email Authentication Failure",
                description="SPF, DKIM, or DMARC failed. The sender address is likely spoofed.",
                severity="CRITICAL"
            ))
        elif auth.get("spf") == "unknown" and auth.get("dkim") == "unknown":
            self.findings.append(Finding(
                title="Missing Authentication",
                description="No SPF or DKIM signatures found. This is common in spam/phishing.",
                severity="MEDIUM"
            ))
            
        # --- Subject / Content Analysis ---
        subject = parsed.get("subject", "").lower()
        body = (parsed.get("body_text", "") + parsed.get("body_html", "")).lower()
        
        urgency_keywords = ['urgent', 'immediate action', 'suspended', 'invoice', 'payment required']
        found_urgency = [kw for kw in urgency_keywords if kw in subject or kw in body]
        
        if found_urgency:
            self.findings.append(Finding(
                title="Social Engineering Indicators",
                description=f"Detected high-risk urgency/financial keywords: {', '.join(found_urgency)}",
                severity="HIGH"
            ))
            
        # --- Attachment Analysis ---
        attachments = parsed.get("attachments", [])
        dangerous_exts = ['.exe', '.scr', '.js', '.vbs', '.bat', '.wsf']
        
        for att in attachments:
            fname = att.get("filename", "").lower()
            if any(fname.endswith(ext) for ext in dangerous_exts):
                self.findings.append(Finding(
                    title="Malicious Attachment Type",
                    description=f"Attached file '{fname}' has a dangerous extension often used for malware delivery.",
                    severity="CRITICAL"
                ))
                break # Only flag once to avoid score bloat

        # --- Link Analysis ---
        urls = parsed.get("urls_extracted", [])
        if len(urls) > 5:
            self.findings.append(Finding(
                title="Excessive Links",
                description=f"Email contains {len(urls)} URLs. Bulk phishing emails often contain many links.",
                severity="LOW"
            ))
            
    def score(self) -> None:
        """Calculate the risk score."""
        base_score = 0
        weights = {"CRITICAL": 60, "HIGH": 30, "MEDIUM": 15, "LOW": 5}
        
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

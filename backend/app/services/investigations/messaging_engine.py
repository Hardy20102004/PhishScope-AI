from typing import Optional

from app.schemas.investigation import Finding
from app.services.investigations.collectors.message_parser import MessageParserCollector
from app.services.investigations.pipeline import BaseInvestigationEngine
from app.services.investigations.url_engine import URLEngine


class MessagingEngine(BaseInvestigationEngine):
    
    def __init__(self, target: str, raw_content: Optional[str] = None):
        # We can accept the message text in target or raw_content
        super().__init__(target)
        self.raw_content = raw_content or target
    
    def validate(self) -> bool:
        if not self.raw_content:
            self.error_message = "No message text provided."
            return False
        return True
            
    def collect_evidence(self) -> None:
        """
        Parses the raw message text.
        """
        parser = MessageParserCollector()
        parsed_data = parser.collect(self.raw_content)
        
        self.evidence["parsed"] = parsed_data
        self.evidence["url_analysis"] = {}
        
        # Reuse URL Engine for extracted links
        urls = parsed_data.get("urls", [])
        for url in urls:
            url_engine = URLEngine(target=url)
            if url_engine.run_pipeline():
                self.evidence["url_analysis"][url] = {
                    "risk_score": url_engine.risk_score,
                    "risk_level": url_engine.risk_level,
                    "evidence": url_engine.evidence
                }
                # Prepend indicator that this came from an embedded URL
                for finding in url_engine.findings:
                    finding.title = f"[Nested URL] {finding.title}"
                    self.findings.append(finding)
        
    def analyze(self) -> None:
        """Analyze the collected evidence and generate findings."""
        parsed = self.evidence.get("parsed", {})
        text = parsed.get("raw_text", "").lower()
        
        # --- Smishing Content Analysis ---
        financial_keywords = [
            'bank', 'account locked', 'verify', 'update your billing', 'unauthorized login',
            'offer', 'miss out', 'win', 'claim', 'urgent', 'act now', 'suspended', 'free', 'gift'
        ]
        found_financial = [kw for kw in financial_keywords if kw in text]
        
        if found_financial:
            self.findings.append(Finding(
                title="Financial Fraud/Smishing Indicator",
                description=f"Detected high-risk financial keywords: {', '.join(found_financial)}",
                severity="HIGH"
            ))
            
        delivery_keywords = ['usps', 'ups', 'fedex', 'package', 'delivery fee', 'missed delivery']
        found_delivery = [kw for kw in delivery_keywords if kw in text]
        
        if found_delivery:
            self.findings.append(Finding(
                title="Delivery Scam Indicator",
                description=f"Detected delivery service impersonation keywords: {', '.join(found_delivery)}",
                severity="MEDIUM"
            ))
            
    def score(self) -> None:
        """Calculate the risk score."""
        base_score = 0
        weights = {"CRITICAL": 70, "HIGH": 40, "MEDIUM": 20, "LOW": 5}
        
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

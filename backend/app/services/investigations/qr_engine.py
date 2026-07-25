from typing import Optional

from app.schemas.investigation import Finding
from app.services.investigations.collectors.qr_decoder import QRDecoderCollector
from app.services.investigations.pipeline import BaseInvestigationEngine
from app.services.investigations.url_engine import URLEngine


class QREngine(BaseInvestigationEngine):
    
    def __init__(self, target: str, raw_content: Optional[str] = None):
        super().__init__(target)
        self.raw_content = raw_content
    
    def validate(self) -> bool:
        if not self.raw_content:
            self.error_message = "No Base64 image payload provided."
            return False
        return True
            
    def collect_evidence(self) -> None:
        """
        Decodes the QR image.
        """
        decoder = QRDecoderCollector()
        decoded_data = decoder.collect(self.raw_content)
        
        self.evidence["qr"] = decoded_data
        self.evidence["url_analysis"] = {}
        
        payload = decoded_data.get("decoded_text", "")
        
        # If the QR code payload is a URL, run the URL engine on it
        if payload and payload.startswith(("http://", "https://")):
            url_engine = URLEngine(target=payload)
            if url_engine.run_pipeline():
                self.evidence["url_analysis"][payload] = {
                    "risk_score": url_engine.risk_score,
                    "risk_level": url_engine.risk_level,
                    "evidence": url_engine.evidence
                }
                for finding in url_engine.findings:
                    finding.title = f"[Nested URL] {finding.title}"
                    self.findings.append(finding)
        
    def analyze(self) -> None:
        """Analyze the collected evidence and generate findings."""
        qr_ev = self.evidence.get("qr", {})
        
        if qr_ev.get("error"):
             self.findings.append(Finding(
                title="QR Decode Error",
                description=f"Failed to extract payload: {qr_ev['error']}",
                severity="MEDIUM"
            ))
             return
             
        payload = qr_ev.get("decoded_text", "")
        
        # Obfuscation checks
        if payload and not payload.startswith(("http://", "https://")):
            if "WIFI:" in payload.upper():
                self.findings.append(Finding(
                    title="Wi-Fi QR Code",
                    description="This is a Wi-Fi connection QR code. Ensure it belongs to a trusted network.",
                    severity="LOW"
                ))
            else:
                self.findings.append(Finding(
                    title="Non-URL Payload",
                    description="The QR code contains raw text or a custom URI scheme.",
                    severity="LOW"
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

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.schemas.investigation import Finding


class BaseInvestigationEngine(ABC):
    """
    The abstract base class for all Investigation Engines (URL, Email, File, etc).
    Enforces a strict pipeline: validate -> collect -> analyze -> score.
    """
    
    def __init__(self, target: str):
        self.target = target
        self.evidence: Dict[str, Any] = {}
        self.findings: List[Finding] = []
        self.risk_score: int = 0
        self.risk_level: str = "UNKNOWN"
        self.error_message: str | None = None
        
    @abstractmethod
    def validate(self) -> bool:
        """Validate the input target (e.g. SSRF checks, format checks)."""
        pass
        
    @abstractmethod
    def collect_evidence(self) -> None:
        """Perform the actual data collection (HTTP requests, file parsing, etc)."""
        pass
        
    @abstractmethod
    def analyze(self) -> None:
        """Run heuristics against the collected evidence to generate Findings."""
        pass
        
    @abstractmethod
    def score(self) -> None:
        """Calculate the final risk score based on the Findings."""
        pass
        
    def run_pipeline(self) -> bool:
        """Executes the standard pipeline. Returns True if successful, False if failed."""
        try:
            if not self.validate():
                return False
                
            self.collect_evidence()
            self.analyze()
            self.score()
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False

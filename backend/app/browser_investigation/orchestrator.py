import logging
from typing import Any, Dict

from app.browser_investigation.ai_integration import BrowserAIIntegration
from app.browser_investigation.engines.cookie import CookieAnalysisEngine
from app.browser_investigation.engines.download import DownloadAnalysisEngine
from app.browser_investigation.engines.extension import ExtensionAnalysisEngine
from app.browser_investigation.engines.history import HistoryAnalysisEngine
from app.browser_investigation.engines.ioc import IOCExtractionEngine
from app.browser_investigation.engines.parser import ProfileParserEngine
from app.browser_investigation.engines.risk import RiskAssessmentEngine
from app.browser_investigation.engines.timeline import TimelineEngine

logger = logging.getLogger(__name__)

class BrowserInvestigationManager:
    """
    Coordinates the execution of Browser Intelligence Engines.
    """
    
    @staticmethod
    async def run_investigation(export_payload: str) -> Dict[str, Any]:
        logger.info("Starting Browser Forensic Investigation")
        
        # 1. Parse Data
        parsed_data = ProfileParserEngine.parse(export_payload)
        
        # 2. Extract Entities
        history = HistoryAnalysisEngine.extract(parsed_data)
        cookies = CookieAnalysisEngine.extract(parsed_data)
        extensions = ExtensionAnalysisEngine.extract(parsed_data)
        downloads = DownloadAnalysisEngine.extract(parsed_data)
        
        # 3. Correlate
        timeline = TimelineEngine.build(history, cookies, downloads)
        iocs = IOCExtractionEngine.extract(history, downloads)
        
        # 4. Score Risk
        risk_score = RiskAssessmentEngine.calculate(extensions, downloads)
        
        # 5. AI Integration
        try:
            ai_summary = await BrowserAIIntegration.generate_narrative(
                extensions=extensions,
                timeline=timeline,
                iocs=iocs,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"risk_narrative": "AI unavailable.", "threat_summary": "Unknown"}
            
        return {
            "history": history,
            "cookies": cookies,
            "extensions": extensions,
            "downloads": downloads,
            "timeline": timeline,
            "iocs": iocs,
            "risk_score": risk_score,
            "ai_summary": ai_summary
        }

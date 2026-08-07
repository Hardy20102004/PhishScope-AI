import logging
from typing import Any, Dict

from app.mobile_investigation.ai_integration import MobileAIIntegration
from app.mobile_investigation.engines.application import ApplicationAnalysisEngine
from app.mobile_investigation.engines.artifact import ArtifactProcessingEngine
from app.mobile_investigation.engines.communication import CommunicationAnalysisEngine
from app.mobile_investigation.engines.ioc import IOCExtractionEngine
from app.mobile_investigation.engines.location import LocationAnalysisEngine
from app.mobile_investigation.engines.metadata import DeviceMetadataEngine
from app.mobile_investigation.engines.risk import RiskAssessmentEngine
from app.mobile_investigation.engines.timeline import TimelineEngine

logger = logging.getLogger(__name__)

class MobileInvestigationManager:
    """
    Coordinates the execution of Mobile Intelligence Engines.
    """
    
    @staticmethod
    async def run_investigation(export_payload: str) -> Dict[str, Any]:
        logger.info("Starting Mobile Forensic Investigation")
        
        # 1. Parse Data
        parsed_data = ArtifactProcessingEngine.parse(export_payload)
        
        # 2. Extract Entities
        metadata = DeviceMetadataEngine.extract(parsed_data)
        applications = ApplicationAnalysisEngine.analyze(parsed_data)
        communications = CommunicationAnalysisEngine.extract(parsed_data)
        locations = LocationAnalysisEngine.extract(parsed_data)
        
        # 3. Correlate
        timeline = TimelineEngine.build(communications, locations)
        iocs = IOCExtractionEngine.extract(communications)
        
        # 4. Score Risk
        risk_score = RiskAssessmentEngine.calculate(applications, iocs)
        
        # 5. AI Integration
        try:
            ai_summary = await MobileAIIntegration.generate_narrative(
                metadata=metadata,
                applications=applications,
                timeline=timeline,
                iocs=iocs,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"risk_narrative": "AI unavailable.", "threat_summary": "Unknown"}
            
        return {
            "device_metadata": metadata,
            "applications": applications,
            "communications": communications,
            "locations": locations,
            "timeline": timeline,
            "iocs": iocs,
            "risk_score": risk_score,
            "ai_summary": ai_summary
        }

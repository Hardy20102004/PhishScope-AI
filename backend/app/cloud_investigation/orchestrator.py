import logging
from typing import Dict, Any

from app.cloud_investigation.engines.parser import CloudArtifactParserEngine
from app.cloud_investigation.engines.asset import CloudAssetEngine
from app.cloud_investigation.engines.identity import CloudIdentityEngine
from app.cloud_investigation.engines.configuration import ConfigurationAnalysisEngine
from app.cloud_investigation.engines.audit import AuditLogAnalysisEngine
from app.cloud_investigation.engines.timeline import TimelineEngine
from app.cloud_investigation.engines.ioc import IOCExtractionEngine
from app.cloud_investigation.engines.risk import RiskAssessmentEngine
from app.cloud_investigation.ai_integration import CloudAIIntegration

logger = logging.getLogger(__name__)

class CloudInvestigationManager:
    """
    Coordinates the execution of Cloud Intelligence Engines.
    """
    
    @staticmethod
    async def run_investigation(export_payload: str) -> Dict[str, Any]:
        logger.info("Starting Cloud Forensic Investigation")
        
        # 1. Parse Data
        parsed_data = CloudArtifactParserEngine.parse(export_payload)
        
        # 2. Extract Entities
        assets = CloudAssetEngine.extract(parsed_data)
        identities = CloudIdentityEngine.extract(parsed_data)
        configurations = ConfigurationAnalysisEngine.extract(parsed_data)
        audit_logs = AuditLogAnalysisEngine.extract(parsed_data)
        
        # 3. Correlate
        timeline = TimelineEngine.build(assets, identities, configurations, audit_logs)
        iocs = IOCExtractionEngine.extract(audit_logs)
        
        # 4. Score Risk
        risk_score = RiskAssessmentEngine.calculate(assets, identities, configurations, audit_logs)
        
        # 5. AI Integration
        try:
            ai_summary = await CloudAIIntegration.generate_narrative(
                identities=identities,
                audit_logs=audit_logs,
                timeline=timeline,
                iocs=iocs,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"risk_narrative": "AI unavailable.", "threat_summary": "Unknown"}
            
        return {
            "assets": assets,
            "identities": identities,
            "configurations": configurations,
            "audit_logs": audit_logs,
            "timeline": timeline,
            "iocs": iocs,
            "risk_score": risk_score,
            "ai_summary": ai_summary
        }

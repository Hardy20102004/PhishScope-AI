import logging
from typing import Dict, Any

from app.network_investigation.engines.parser import PCAPProcessingEngine
from app.network_investigation.engines.flow import FlowAnalysisEngine
from app.network_investigation.engines.dns import DNSAnalysisEngine
from app.network_investigation.engines.http import HTTPAnalysisEngine
from app.network_investigation.engines.tls import TLSAnalysisEngine
from app.network_investigation.engines.timeline import TimelineEngine
from app.network_investigation.engines.ioc import IOCExtractionEngine
from app.network_investigation.engines.risk import RiskAssessmentEngine
from app.network_investigation.ai_integration import NetworkAIIntegration

logger = logging.getLogger(__name__)

class NetworkInvestigationManager:
    """
    Coordinates the execution of Network Intelligence Engines.
    """
    
    @staticmethod
    async def run_investigation(export_payload: str) -> Dict[str, Any]:
        logger.info("Starting Network Forensic Investigation")
        
        # 1. Parse Data
        parsed_data = PCAPProcessingEngine.parse(export_payload)
        
        # 2. Extract Entities
        flows = FlowAnalysisEngine.extract(parsed_data)
        dns = DNSAnalysisEngine.extract(parsed_data)
        http = HTTPAnalysisEngine.extract(parsed_data)
        tls = TLSAnalysisEngine.extract(parsed_data)
        
        # 3. Correlate
        timeline = TimelineEngine.build(flows, dns, http, tls)
        iocs = IOCExtractionEngine.extract(dns, http, tls)
        
        # 4. Score Risk
        risk_score = RiskAssessmentEngine.calculate(dns, http)
        
        # 5. AI Integration
        try:
            ai_summary = await NetworkAIIntegration.generate_narrative(
                dns=dns,
                http=http,
                timeline=timeline,
                iocs=iocs,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"risk_narrative": "AI unavailable.", "threat_summary": "Unknown"}
            
        return {
            "flows": flows,
            "dns": dns,
            "http": http,
            "tls": tls,
            "timeline": timeline,
            "iocs": iocs,
            "risk_score": risk_score,
            "ai_summary": ai_summary
        }

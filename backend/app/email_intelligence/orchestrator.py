import logging
from typing import Any, Dict

from app.email_intelligence.ai_integration import EmailAIIntegration
from app.email_intelligence.engines.attachments import AttachmentIntelligenceEngine
from app.email_intelligence.engines.auth import AuthenticationAnalysisEngine
from app.email_intelligence.engines.campaign import CampaignCorrelationEngine
from app.email_intelligence.engines.conversation import ConversationAnalysisEngine
from app.email_intelligence.engines.headers import HeaderAnalysisEngine
from app.email_intelligence.engines.parser import EmailParserEngine
from app.email_intelligence.engines.routing import RoutingAnalysisEngine
from app.email_intelligence.engines.scoring import EmailRiskScoringEngine

logger = logging.getLogger(__name__)

class EmailInvestigationOrchestrator:
    """
    Coordinates the execution of Email Intelligence Engines.
    """
    
    @staticmethod
    async def run_investigation(raw_eml: str) -> Dict[str, Any]:
        logger.info("Starting Email Investigation")
        
        # 1. Parse Raw EML
        parsed_data = EmailParserEngine.parse(raw_eml)
        if parsed_data.get("error"):
            return {"error": parsed_data["error"]}
            
        raw_headers = parsed_data.get("headers", {})
        
        # 2. Execute Engines
        header_data = HeaderAnalysisEngine.analyze(raw_headers)
        auth_data = AuthenticationAnalysisEngine.analyze(raw_headers)
        routing_data = RoutingAnalysisEngine.analyze(raw_headers)
        
        conversation_data = ConversationAnalysisEngine.analyze(
            parsed_data.get("body_text", ""), 
            parsed_data.get("body_html", "")
        )
        
        attachment_data = AttachmentIntelligenceEngine.analyze(parsed_data.get("attachments", []))
        
        campaign_data = CampaignCorrelationEngine.analyze(header_data, conversation_data.get("extracted_urls", []))
        
        # 3. Risk Scoring
        risk_score = EmailRiskScoringEngine.calculate(
            auth=auth_data,
            conversation=conversation_data,
            attachments=attachment_data,
            campaign=campaign_data
        )
        
        # 4. AI Integration
        try:
            ai_summary = await EmailAIIntegration.generate_narrative(
                headers=header_data,
                auth=auth_data,
                conversation=conversation_data,
                attachments=attachment_data,
                campaign=campaign_data,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"risk_narrative": "AI unavailable.", "threat_summary": "Unknown"}
            
        return {
            "header_data": header_data,
            "auth_results": auth_data,
            "routing_hops": routing_data,
            "conversation_analysis": conversation_data,
            "attachments": attachment_data,
            "campaign_correlation": campaign_data,
            "risk_score": risk_score,
            "ai_summary": ai_summary
        }

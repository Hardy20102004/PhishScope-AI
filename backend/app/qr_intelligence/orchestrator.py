import logging
from typing import Dict, Any

from app.qr_intelligence.engines.decoder import QRDecoderEngine
from app.qr_intelligence.engines.image import ImageProcessingEngine
from app.qr_intelligence.engines.visual import VisualAnalysisEngine
from app.qr_intelligence.engines.tampering import TamperingDetectionEngine
from app.qr_intelligence.engines.payment import PaymentQRAnalyzer
from app.qr_intelligence.engines.scoring import QRRiskScoringEngine
from app.qr_intelligence.ai_integration import QRAIIntegration

logger = logging.getLogger(__name__)

class QRInvestigationOrchestrator:
    """
    Coordinates the execution of QR Intelligence Engines.
    """
    
    @staticmethod
    async def run_investigation(raw_payload_input: str) -> Dict[str, Any]:
        logger.info("Starting QR Investigation")
        
        # 1. Image Processing (Mocked using bytes)
        image_data = ImageProcessingEngine.analyze(b"mock_image_data")
        
        # 2. Decode Payload
        decoded_payload = QRDecoderEngine.decode(raw_payload_input)
        
        # 3. Analyze
        visual_data = VisualAnalysisEngine.analyze(decoded_payload)
        tampering_data = TamperingDetectionEngine.analyze(decoded_payload)
        payment_data = PaymentQRAnalyzer.analyze(decoded_payload)
        
        # URL Integration (Mocked trigger here, but in reality would await url_intelligence)
        url_risk_score = 0
        if decoded_payload.get("payload_type") == "url":
            url_risk_score = 50 # Mocked high risk for prototype
            
        # 4. Risk Scoring
        risk_score = QRRiskScoringEngine.calculate(
            tampering=tampering_data,
            payment=payment_data,
            visual=visual_data,
            url_risk_score=url_risk_score
        )
        
        # 5. AI Integration
        try:
            ai_summary = await QRAIIntegration.generate_narrative(
                decoded=decoded_payload,
                visual=visual_data,
                tampering=tampering_data,
                payment=payment_data,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"risk_narrative": "AI unavailable.", "threat_summary": "Unknown"}
            
        return {
            "image_metadata": image_data,
            "decoded_payload": decoded_payload,
            "visual_analysis": visual_data,
            "tampering_analysis": tampering_data,
            "payment_analysis": payment_data,
            "risk_score": risk_score,
            "ai_summary": ai_summary
        }

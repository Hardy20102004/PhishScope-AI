"""
ai_integration.py
-----------------
URL Intelligence AI Integration — now powered by Google Gemini.

Replaces the previous hardcoded string-builder with real Gemini API calls.
Supports all Gemini model versions with automatic fallback.
"""
import logging
from typing import Any, Dict

from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)


class URLAIIntegration:
    """
    Integrates URL Intelligence with Google Gemini AI to generate
    explainable, evidence-backed threat narratives.
    
    Now powered by real Gemini models:
    - gemini-2.5-pro (primary, deep analysis)
    - gemini-2.5-flash (fast triage)
    - gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash (fallbacks)
    """
    
    @staticmethod
    async def generate_narrative(
        url: str,
        intel: dict,
        brand: dict,
        infra: dict,
        risk: dict
    ) -> Dict[str, Any]:
        """
        Generates a Gemini-powered threat narrative based on collected investigation evidence.
        
        Returns a rich analysis dict including:
        - risk_narrative: Plain English explanation
        - threat_summary: Active threat categories
        - recommended_next_steps: Action for UP Police Cyber Cell
        - evidence_correlation: Technical evidence linkage
        - iocs: Indicators of Compromise
        - confidence_adjusted_severity: Gemini's severity assessment
        - gemini_risk_score: AI-computed 0-100 risk score
        - report_summary_hindi: Hindi summary for police reports
        - model_used: Which Gemini model produced the analysis
        - ai_provider: "Google Gemini" or "PhishScope Rule Engine" (fallback)
        """
        logger.info(
            f"Invoking Gemini AI analysis for URL: {url} | "
            f"Gemini available: {gemini_service.is_available} | "
            f"Active model: {gemini_service.active_model}"
        )
        
        try:
            result = await gemini_service.analyze_phishing_threat(
                url=url,
                intel_data=intel,
                brand_data=brand,
                infra_data=infra,
                risk_data=risk,
            )
            return result
        except Exception as e:
            logger.error(f"Gemini AI integration failed with unexpected error: {e}", exc_info=True)
            # Return a safe minimal response — never crash the investigation
            return {
                "risk_narrative": f"AI analysis encountered an error for {url}. Manual review required.",
                "threat_summary": "Unknown — AI error",
                "recommended_next_steps": "Conduct manual investigation. AI service temporarily unavailable.",
                "evidence_correlation": f"Error: {str(e)}",
                "iocs": [],
                "confidence_adjusted_severity": risk.get("threat_severity", "UNKNOWN"),
                "gemini_risk_score": risk.get("overall_risk_score", 0),
                "model_used": "error_fallback",
                "ai_provider": "Error",
                "report_summary_hindi": "AI विश्लेषण में त्रुटि — मैनुअल समीक्षा आवश्यक है।",
            }

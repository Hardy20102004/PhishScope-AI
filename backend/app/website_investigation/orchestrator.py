import logging
from typing import Any, Dict

from app.website_investigation.ai_integration import WebsiteAIIntegration
from app.website_investigation.engines.fetcher import PageFetchEngine
from app.website_investigation.engines.forms_cookies import CookieAnalysisEngine, FormAnalysisEngine
from app.website_investigation.engines.html import HTMLAnalysisEngine
from app.website_investigation.engines.javascript import JavaScriptAnalysisEngine
from app.website_investigation.engines.scoring import WebsiteRiskScoringEngine
from app.website_investigation.engines.security import SecurityHeaderAnalyzer
from app.website_investigation.engines.visual import VisualAnalysisEngine

logger = logging.getLogger(__name__)

class WebsiteInvestigationOrchestrator:
    """
    Coordinates the execution of Website Intelligence Engines.
    """
    
    @staticmethod
    async def run_investigation(url: str) -> Dict[str, Any]:
        logger.info(f"Starting Website investigation for: {url}")
        
        # 1. Fetch Page Data (HTML, DOM, JS, Cookies, Headers, Forms)
        snapshot = await PageFetchEngine.fetch(url)
        
        if snapshot.get("error"):
            return {"error": snapshot["error"], "url": url}
            
        html_content = snapshot.get("html", "")
        headers = snapshot.get("headers", {})
        forms = snapshot.get("forms", [])
        scripts = snapshot.get("scripts", [])
        cookies = snapshot.get("cookies", [])
        title = snapshot.get("title", "")
        
        # 2. Extract & Analyze
        html_data = HTMLAnalysisEngine.analyze(html_content)
        js_data = JavaScriptAnalysisEngine.analyze(scripts)
        form_data = FormAnalysisEngine.analyze(forms)
        cookie_data = CookieAnalysisEngine.analyze(cookies)
        security_data = SecurityHeaderAnalyzer.analyze(headers)
        visual_data = VisualAnalysisEngine.analyze(url, title)
        
        # 3. Risk Scoring
        risk_score = WebsiteRiskScoringEngine.calculate(
            html=html_data,
            js=js_data,
            forms=form_data,
            cookies=cookie_data,
            security=security_data,
            visual=visual_data
        )
        
        # 4. AI Integration
        try:
            ai_summary = await WebsiteAIIntegration.generate_narrative(
                url=url,
                html=html_data,
                js=js_data,
                forms=form_data,
                security=security_data,
                visual=visual_data,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"risk_narrative": "AI unavailable.", "threat_summary": "Unknown"}
            
        return {
            "url": url,
            "snapshot_metadata": {
                "title": title,
                "description": snapshot.get("description", ""),
                "language": snapshot.get("language", ""),
                "status_code": snapshot.get("status_code")
            },
            "html_analysis": html_data,
            "javascript_analysis": js_data,
            "form_analysis": form_data,
            "cookie_analysis": cookie_data,
            "security_headers": security_data,
            "visual_analysis": visual_data,
            "risk_score": risk_score,
            "ai_summary": ai_summary,
            # We don't send the full raw HTML back to the frontend to keep payload size small
            # just the analysis results. If needed, a separate endpoint would serve the raw code.
        }

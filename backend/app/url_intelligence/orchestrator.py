import asyncio
import logging
import time
from typing import Any, Dict

from app.url_intelligence.ai_integration import URLAIIntegration
from app.url_intelligence.engines.brand import BrandProtectionEngine
from app.url_intelligence.engines.infrastructure import InfrastructureCorrelationEngine
from app.url_intelligence.engines.intelligence import URLIntelligenceEngine
from app.url_intelligence.engines.normalizer import URLNormalizationEngine
from app.url_intelligence.engines.parser import URLParser
from app.url_intelligence.engines.redirect import RedirectAnalysisEngine
from app.url_intelligence.engines.scoring import RiskScoringEngine

logger = logging.getLogger(__name__)


class InvestigationOrchestrator:
    """
    Coordinates execution of all URL Intelligence Engines.
    Supports asynchronous parallel lookups and incremental enrichment.
    
    Updated (v2):
    - Added investigation timing metadata
    - Improved AI error fallback with structured response
    - Brand engine receives both hostname and root_domain for accuracy
    - All async tasks properly gathered in parallel
    """
    
    @staticmethod
    async def run_investigation(url: str) -> Dict[str, Any]:
        start_time = time.monotonic()
        logger.info(f"Starting URL investigation for: {url}")
        
        # 1. Parsing & Normalization (synchronous, fast)
        canonical_url = URLNormalizationEngine.normalize(url)
        parsed_data = URLParser.parse(canonical_url)
        
        hostname = parsed_data.get("hostname", "")
        root_domain = parsed_data.get("root_domain", "")
        
        logger.info(f"Parsed: hostname={hostname}, root_domain={root_domain}")
        
        # 2. Base URL Intelligence (synchronous, CPU-bound)
        intel_data = URLIntelligenceEngine.analyze(canonical_url, parsed_data)
        
        # 3. Parallel Async Lookups — redirect chain + full DNS/TLS/infra
        redirect_task = asyncio.create_task(RedirectAnalysisEngine.analyze(canonical_url))
        infra_task = asyncio.create_task(InfrastructureCorrelationEngine.analyze(hostname))
        
        redirect_chain, infra_data = await asyncio.gather(
            redirect_task, infra_task, return_exceptions=False
        )
        
        # Handle cases where infra returned an exception
        if isinstance(infra_data, Exception):
            logger.warning(f"Infrastructure lookup failed: {infra_data}")
            infra_data = {"domain_name": hostname, "ips": [], "nameservers": [], "mx_records": [], "txt_records": [], "certificates": []}
        
        if isinstance(redirect_chain, Exception):
            logger.warning(f"Redirect analysis failed: {redirect_chain}")
            redirect_chain = []
        
        # 4. Brand Protection Analysis
        brand_data = BrandProtectionEngine.analyze(hostname, root_domain)
        
        # 5. Risk Scoring — aggregates all signals
        risk_score = RiskScoringEngine.calculate(intel_data, brand_data, infra_data)
        
        # 6. Gemini AI Narrative Generation
        try:
            ai_summary = await URLAIIntegration.generate_narrative(
                url=canonical_url,
                intel=intel_data,
                brand=brand_data,
                infra=infra_data,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}", exc_info=True)
            ai_summary = {
                "risk_narrative": "AI narrative generation unavailable.",
                "threat_summary": "Unknown",
                "recommended_next_steps": "Manual review required.",
                "evidence_correlation": "AI service error.",
                "iocs": [],
                "confidence_adjusted_severity": risk_score.get("threat_severity", "UNKNOWN"),
                "gemini_risk_score": risk_score.get("overall_risk_score", 0),
                "model_used": "error_fallback",
                "ai_provider": "Error",
                "report_summary_hindi": "AI विश्लेषण अनुपलब्ध",
            }
        
        elapsed_ms = round((time.monotonic() - start_time) * 1000)
        logger.info(f"Investigation complete for {url} in {elapsed_ms}ms")
        
        return {
            "canonical_url": canonical_url,
            "parsed": parsed_data,
            "intelligence": intel_data,
            "redirect_chain": redirect_chain,
            "infrastructure": infra_data,
            "brand": brand_data,
            "risk_score": risk_score,
            "ai_summary": ai_summary,
            "investigation_time_ms": elapsed_ms,
        }

import asyncio
from typing import Dict, Any
import logging

from app.url_intelligence.engines.parser import URLParser
from app.url_intelligence.engines.normalizer import URLNormalizationEngine
from app.url_intelligence.engines.intelligence import URLIntelligenceEngine
from app.url_intelligence.engines.redirect import RedirectAnalysisEngine
from app.url_intelligence.engines.infrastructure import InfrastructureCorrelationEngine
from app.url_intelligence.engines.brand import BrandProtectionEngine
from app.url_intelligence.engines.scoring import RiskScoringEngine
from app.url_intelligence.ai_integration import URLAIIntegration

logger = logging.getLogger(__name__)

class InvestigationOrchestrator:
    """
    Coordinates the execution of URL Intelligence Engines.
    Supports asynchronous parallel lookups and incremental enrichment.
    """
    
    @staticmethod
    async def run_investigation(url: str) -> Dict[str, Any]:
        logger.info(f"Starting URL investigation for: {url}")
        
        # 1. Parsing & Normalization (Synchronous, fast)
        canonical_url = URLNormalizationEngine.normalize(url)
        parsed_data = URLParser.parse(canonical_url)
        
        # 2. Base Intelligence
        intel_data = URLIntelligenceEngine.analyze(canonical_url, parsed_data)
        
        # 3. Parallel Async Lookups
        hostname = parsed_data.get("hostname", "")
        root_domain = parsed_data.get("root_domain", "")
        
        # Run Redirect and Infrastructure in parallel
        redirect_task = asyncio.create_task(RedirectAnalysisEngine.analyze(canonical_url))
        infra_task = asyncio.create_task(InfrastructureCorrelationEngine.analyze(hostname))
        
        redirect_chain, infra_data = await asyncio.gather(redirect_task, infra_task)
        
        # 4. Brand Protection
        brand_data = BrandProtectionEngine.analyze(hostname, root_domain)
        
        # 5. Risk Scoring
        risk_score = RiskScoringEngine.calculate(intel_data, brand_data, infra_data)
        
        # 6. AI Integration for Narrative (if applicable)
        try:
            ai_summary = await URLAIIntegration.generate_narrative(
                url=canonical_url,
                intel=intel_data,
                brand=brand_data,
                infra=infra_data,
                risk=risk_score
            )
        except Exception as e:
            logger.error(f"AI integration failed: {e}")
            ai_summary = {"narrative": "AI generation unavailable.", "threat_summary": "Unknown"}
            
        return {
            "canonical_url": canonical_url,
            "parsed": parsed_data,
            "intelligence": intel_data,
            "redirect_chain": redirect_chain,
            "infrastructure": infra_data,
            "brand": brand_data,
            "risk_score": risk_score,
            "ai_summary": ai_summary
        }

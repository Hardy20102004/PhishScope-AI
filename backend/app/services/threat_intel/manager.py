import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.threat_intel import Indicator, ThreatFeedResult
from app.services.threat_intel.connectors.google_safe_browsing import GoogleSafeBrowsingConnector
from app.services.threat_intel.connectors.virustotal import VirusTotalConnector
from app.services.threat_intel.normalization import IndicatorNormalizationEngine
from app.services.threat_intel.reputation import ReputationEngine


class ThreatIntelManager:
    """Orchestrates threat intelligence gathering and caching."""
    
    def __init__(self, db: Session):
        self.db = db
        # In a real app, these would be injected or loaded dynamically
        self.connectors = [
            VirusTotalConnector(),
            GoogleSafeBrowsingConnector()
        ]
        
    async def get_indicator(self, value: str, force_refresh: bool = False) -> Indicator:
        """
        Get intelligence for an indicator. 
        Will use cache if valid, otherwise queries feeds.
        """
        indicator_type = IndicatorNormalizationEngine.identify_type(value)
        normalized_value = IndicatorNormalizationEngine.normalize(value, indicator_type)
        
        # Check DB first
        stmt = select(Indicator).where(Indicator.normalized_value == normalized_value)
        indicator = self.db.execute(stmt).scalar_one_or_none()
        
        needs_refresh = False
        if not indicator:
            # Create new indicator
            indicator = Indicator(
                value=value,
                type=indicator_type,
                normalized_value=normalized_value
            )
            self.db.add(indicator)
            self.db.commit()
            self.db.refresh(indicator)
            needs_refresh = True
        else:
            # Check if cache is expired (e.g., older than 24 hours)
            last_updated = indicator.last_updated
            if last_updated and last_updated.tzinfo is None:
                last_updated = last_updated.replace(tzinfo=timezone.utc)
            if not last_updated or (datetime.now(timezone.utc) - last_updated > timedelta(hours=24)):
                needs_refresh = True
                
        if force_refresh or needs_refresh:
            await self._refresh_indicator(indicator)
            
        return indicator
        
    async def _refresh_indicator(self, indicator: Indicator):
        """Query all feeds concurrently and update indicator."""
        
        # Gather tasks
        tasks = []
        for connector in self.connectors:
            tasks.append(self._query_connector(connector, indicator.normalized_value, indicator.type))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        feed_dicts = []
        
        # Process results
        for idx, result in enumerate(results):
            connector = self.connectors[idx]
            
            if isinstance(result, Exception):
                print(f"Error querying {connector.name}: {result}")
                continue
                
            # Clear old result for this source if exists
            stmt = select(ThreatFeedResult).where(
                ThreatFeedResult.indicator_id == indicator.id,
                ThreatFeedResult.source == connector.name
            )
            old_result = self.db.execute(stmt).scalar_one_or_none()
            if old_result:
                self.db.delete(old_result)
                
            # Create new result
            new_result = ThreatFeedResult(
                indicator_id=indicator.id,
                source=connector.name,
                reputation_score=result.get("reputation_score", 0.0),
                confidence=result.get("confidence", 0.0),
                threat_classification=result.get("threat_classification"),
                raw_data=result.get("raw_data"),
                is_cached=True
            )
            self.db.add(new_result)
            
            feed_dicts.append({
                "source": connector.name,
                "reputation_score": new_result.reputation_score,
                "confidence": new_result.confidence
            })
            
        # Calculate overall reputation
        rep = ReputationEngine.calculate(feed_dicts)
        
        indicator.reputation_score = rep["reputation_score"]
        indicator.confidence_score = rep["confidence_score"]
        indicator.threat_classification = rep["threat_classification"]
        indicator.last_updated = datetime.now(timezone.utc)
        indicator.last_seen = datetime.now(timezone.utc)
        indicator.observation_count += 1
        
        self.db.commit()
        self.db.refresh(indicator)
        
    async def _query_connector(self, connector, value: str, type: str) -> Dict[str, Any]:
        """Wrapper to handle connector query with timeout."""
        try:
            return await asyncio.wait_for(connector.query(value, type), timeout=5.0)
        except asyncio.TimeoutError:
            print(f"Connector {connector.name} timed out")
            return {
                "reputation_score": 0.0,
                "confidence": 0.0,
                "threat_classification": None,
                "raw_data": {"error": "Timeout"}
            }
        except Exception as e:
            print(f"Connector {connector.name} failed: {str(e)}")
            return {
                "reputation_score": 0.0,
                "confidence": 0.0,
                "threat_classification": None,
                "raw_data": {"error": str(e)}
            }

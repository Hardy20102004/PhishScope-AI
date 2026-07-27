import structlog
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.models.predictive import ForecastDomain
from app.schemas.predictive import ThreatForecastCreate, ForecastScenarioCreate, ForecastEvidenceCreate
from app.predictive.manager import PredictionManager
from app.predictive.pattern_discovery import PatternDiscoveryEngine

logger = structlog.get_logger("phoenix.predictive.forecast")

class ForecastEngine:
    """Generates ThreatForecast objects based on discovered patterns."""
    
    def __init__(self, db: Session):
        self.db = db
        self.manager = PredictionManager(db)
        self.pattern_engine = PatternDiscoveryEngine(db)

    def generate_forecasts(self):
        """Runs pattern discovery and compiles them into actionable Forecasts."""
        logger.info("generating_threat_forecasts")
        
        patterns = self.pattern_engine.scan_infrastructure_reuse()
        
        for pattern in patterns:
            # Generate a forecast for Infrastructure Reuse
            now = datetime.now(timezone.utc)
            forecast_req = ThreatForecastCreate(
                title=f"Likely Campaign Resurgence on {pattern['entity_id']}",
                description=pattern['description'],
                domain=ForecastDomain.INFRASTRUCTURE_REUSE,
                confidence_score=pattern['confidence'],
                uncertainty_score=0.3, # Fairly certain if cert is new
                time_horizon_start=now,
                time_horizon_end=now + timedelta(days=14),
                scenarios=[
                    ForecastScenarioCreate(
                        scenario_name="Active Campaign Launch",
                        description="The threat actor will launch a new phishing wave using this domain within 14 days.",
                        probability=0.75
                    ),
                    ForecastScenarioCreate(
                        scenario_name="Infrastructure Staging",
                        description="The domain is being staged for future use but won't be active immediately.",
                        probability=0.25
                    )
                ],
                evidence=[
                    ForecastEvidenceCreate(
                        evidence_type="KNOWLEDGE_GRAPH_NODE",
                        reference_id=pattern['entity_id'],
                        explanation="Domain previously used by APT29. New TLS certificate detected."
                    )
                ]
            )
            self.manager.create_forecast(forecast_req)
            logger.info("forecast_created", title=forecast_req.title)

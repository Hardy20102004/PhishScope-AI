from typing import Optional, List
import structlog
from sqlalchemy.orm import Session

from app.models.predictive import ThreatForecast, ForecastScenario, ForecastEvidence
from app.schemas.predictive import ThreatForecastCreate

logger = structlog.get_logger("phoenix.predictive.manager")

class PredictionManager:
    """Handles CRUD operations for Threat Forecasts."""
    def __init__(self, db: Session):
        self.db = db

    def create_forecast(self, req: ThreatForecastCreate) -> ThreatForecast:
        forecast = ThreatForecast(
            title=req.title,
            description=req.description,
            domain=req.domain,
            tenant_id=req.tenant_id,
            confidence_score=req.confidence_score,
            uncertainty_score=req.uncertainty_score,
            time_horizon_start=req.time_horizon_start,
            time_horizon_end=req.time_horizon_end,
            properties_json=req.properties_json
        )
        self.db.add(forecast)
        
        if req.scenarios:
            for s in req.scenarios:
                scenario = ForecastScenario(
                    forecast=forecast,
                    scenario_name=s.scenario_name,
                    description=s.description,
                    probability=s.probability
                )
                self.db.add(scenario)
                
        if req.evidence:
            for e in req.evidence:
                evidence = ForecastEvidence(
                    forecast=forecast,
                    evidence_type=e.evidence_type,
                    reference_id=e.reference_id,
                    explanation=e.explanation
                )
                self.db.add(evidence)
                
        self.db.commit()
        self.db.refresh(forecast)
        return forecast

    def get_forecast(self, forecast_id: str) -> Optional[ThreatForecast]:
        return self.db.query(ThreatForecast).filter_by(id=forecast_id).first()

    def get_all_forecasts(self, tenant_id: Optional[str] = None) -> List[ThreatForecast]:
        q = self.db.query(ThreatForecast)
        if tenant_id:
            q = q.filter_by(tenant_id=tenant_id)
        return q.order_by(ThreatForecast.created_at.desc()).all()

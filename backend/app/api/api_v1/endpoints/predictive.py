from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api import deps
from app.predictive.manager import PredictionManager
from app.predictive.forecast import ForecastEngine
from app.predictive.trend import TrendAnalysisEngine
from app.schemas.predictive import ThreatForecastCreate, ThreatForecastResponse

router = APIRouter()

@router.get("/forecasts", response_model=List[ThreatForecastResponse])
def get_forecasts(tenant_id: str = None, db: Session = Depends(deps.get_db)):
    manager = PredictionManager(db)
    return manager.get_all_forecasts(tenant_id=tenant_id)

@router.post("/forecasts/generate")
def generate_forecasts(background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    """Triggers the Pattern Discovery and Forecast Engine to generate new predictions."""
    def run_forecast_job():
        from app.db.session import SessionLocal
        bg_db = SessionLocal()
        try:
            engine = ForecastEngine(bg_db)
            engine.generate_forecasts()
        finally:
            bg_db.close()
            
    background_tasks.add_task(run_forecast_job)
    return {"status": "success", "message": "Forecast generation started in background."}

@router.get("/trends/industry", response_model=List[Dict[str, Any]])
def get_industry_trends(db: Session = Depends(deps.get_db)):
    engine = TrendAnalysisEngine(db)
    return engine.get_industry_targeting_trends()

@router.get("/trends/malware", response_model=Dict[str, Any])
def get_malware_trends(db: Session = Depends(deps.get_db)):
    engine = TrendAnalysisEngine(db)
    return engine.get_malware_volume_trends()

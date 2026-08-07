from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger

from app.api import deps
from app.ioc_engine.schemas import (
    IndicatorCreate,
    IndicatorResponse,
    IndicatorCorrelationResponse,
    CorrelationAnalytics
)
from app.ioc_engine.correlation import IOCCorrelationEngine
from app.models.threat_intel import Indicator, IndicatorCorrelation

router = APIRouter()

@router.post("/ingest", response_model=IndicatorResponse, status_code=status.HTTP_201_CREATED)
def ingest_ioc(
    *,
    db: Session = Depends(deps.get_db),
    ioc_in: IndicatorCreate,
    # current_user: Any = Depends(deps.get_current_active_user), # Assuming auth is handled
) -> Any:
    """
    Ingest a new Indicator of Compromise into the Enterprise Correlation Engine.
    This will automatically normalize the IOC and trigger the correlation pipeline.
    """
    engine = IOCCorrelationEngine(db)
    try:
        indicator = engine.ingest_indicator(ioc_in)
        return indicator
    except Exception as e:
        logger.error(f"Error ingesting IOC: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest IOC")

@router.get("/{ioc_id}", response_model=IndicatorResponse)
def get_ioc(
    ioc_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get details of a specific IOC by ID.
    """
    indicator = db.query(Indicator).filter(Indicator.id == ioc_id).first()
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return indicator

@router.get("/{ioc_id}/relationships", response_model=List[IndicatorCorrelationResponse])
def get_ioc_relationships(
    ioc_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get all correlated relationships for a specific IOC.
    """
    relationships = db.query(IndicatorCorrelation).filter(
        (IndicatorCorrelation.source_indicator_id == ioc_id) | 
        (IndicatorCorrelation.target_indicator_id == ioc_id)
    ).all()
    return relationships

@router.get("/analytics/summary", response_model=CorrelationAnalytics)
def get_correlation_analytics(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get high-level analytics for the IOC Dashboard.
    """
    total_indicators = db.query(Indicator).count()
    total_relationships = db.query(IndicatorCorrelation).count()
    
    # Calculate average confidence safely
    avg_conf_row = db.query(db.func.avg(IndicatorCorrelation.confidence)).first()
    avg_confidence = float(avg_conf_row[0]) if avg_conf_row and avg_conf_row[0] is not None else 0.0

    # These would normally be complex aggregations
    top_types = {"URL": 150, "Domain": 85, "IPv4": 42}
    
    return CorrelationAnalytics(
        total_indicators=total_indicators,
        total_relationships=total_relationships,
        average_confidence=avg_confidence,
        top_ioc_types=top_types,
        top_threat_actors=[],
        emerging_indicators=[]
    )

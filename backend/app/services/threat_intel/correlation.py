from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.threat_intel import IndicatorCorrelation

class CorrelationEngine:
    """Finds and links related indicators."""
    
    @staticmethod
    def add_correlation(db: Session, source_id: UUID, target_id: UUID, correlation_type: str, confidence: float = 1.0) -> IndicatorCorrelation:
        """Adds a correlation between two indicators."""
        # Simple implementation for now
        correlation = IndicatorCorrelation(
            source_indicator_id=source_id,
            target_indicator_id=target_id,
            correlation_type=correlation_type,
            confidence=confidence
        )
        db.add(correlation)
        db.commit()
        db.refresh(correlation)
        return correlation

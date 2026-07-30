from typing import List
from sqlalchemy.orm import Session
from app.models.cyber_os import UnifiedObservabilityMetric
from app.schemas.cyber_os import UnifiedObservabilityMetricCreate

class ObservabilityService:
    def __init__(self, db: Session):
        self.db = db

    def record_metric(self, metric_in: UnifiedObservabilityMetricCreate) -> UnifiedObservabilityMetric:
        db_metric = UnifiedObservabilityMetric(
            metric_type=metric_in.metric_type,
            value=metric_in.value,
            unit=metric_in.unit,
            source_module=metric_in.source_module
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric

    def get_metrics(self, skip: int = 0, limit: int = 100) -> List[UnifiedObservabilityMetric]:
        return self.db.query(UnifiedObservabilityMetric).order_by(UnifiedObservabilityMetric.timestamp.desc()).offset(skip).limit(limit).all()

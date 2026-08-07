from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.data_fabric import QualityMetric, QualityStatus
from app.schemas.data_fabric import QualityMetricCreate

class DataQualityEngine:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_quality(self, metric_in: QualityMetricCreate) -> QualityMetric:
        db_metric = QualityMetric(
            node_id=metric_in.node_id,
            completeness_score=metric_in.completeness_score,
            consistency_score=metric_in.consistency_score,
            freshness_score=metric_in.freshness_score,
            accuracy_score=metric_in.accuracy_score,
            overall_status=metric_in.overall_status,
            confidence=metric_in.confidence,
            details=metric_in.details,
            evaluated_at=datetime.now(timezone.utc)
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric

    def get_latest_quality(self, node_id: UUID) -> Optional[QualityMetric]:
        return self.db.query(QualityMetric).filter(
            QualityMetric.node_id == node_id
        ).order_by(QualityMetric.evaluated_at.desc()).first()

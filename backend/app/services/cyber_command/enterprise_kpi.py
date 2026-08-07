from typing import List
from sqlalchemy.orm import Session
from app.models.cyber_command import EnterpriseHealthMetric
from app.schemas.cyber_command import EnterpriseHealthMetricCreate

class EnterpriseKPIEngine:
    def __init__(self, db: Session):
        self.db = db

    def record_metric(self, metric_in: EnterpriseHealthMetricCreate) -> EnterpriseHealthMetric:
        db_metric = EnterpriseHealthMetric(
            domain=metric_in.domain,
            health_score=metric_in.health_score,
            status=metric_in.status,
            details=metric_in.details
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric

    def get_metrics(self, skip: int = 0, limit: int = 100) -> List[EnterpriseHealthMetric]:
        return self.db.query(EnterpriseHealthMetric).offset(skip).limit(limit).all()

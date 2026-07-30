from typing import List
from sqlalchemy.orm import Session
from app.models.cyber_governance import RiskOversightMetric
from app.schemas.cyber_governance import RiskOversightMetricCreate

class RiskOversightEngine:
    def __init__(self, db: Session):
        self.db = db

    def record_risk_metric(self, metric_in: RiskOversightMetricCreate) -> RiskOversightMetric:
        db_metric = RiskOversightMetric(
            risk_domain=metric_in.risk_domain,
            risk_score=metric_in.risk_score,
            confidence_level=metric_in.confidence_level,
            details=metric_in.details
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric

    def get_metrics(self, skip: int = 0, limit: int = 100) -> List[RiskOversightMetric]:
        return self.db.query(RiskOversightMetric).offset(skip).limit(limit).all()

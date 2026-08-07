from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.knowledge_evolution import EvolutionQualityMetric
from app.schemas.knowledge_evolution import EvolutionQualityMetricCreate

class KnowledgeQualityEngine:
    def __init__(self, db: Session):
        self.db = db

    def record_quality(self, metric_in: EvolutionQualityMetricCreate) -> EvolutionQualityMetric:
        db_metric = EvolutionQualityMetric(
            coverage_score=metric_in.coverage_score,
            consistency_score=metric_in.consistency_score,
            freshness_score=metric_in.freshness_score,
            confidence_score=metric_in.confidence_score,
            relationship_quality=metric_in.relationship_quality,
            details=metric_in.details,
            evaluated_at=datetime.now(timezone.utc)
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric

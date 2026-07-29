import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.blue_team import DetectionMetric

class DetectionValidationEngine:
    """
    Analyzes historical SIEM/EDR rule performance and flags noisy or broken logic.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def evaluate_rule_health(self, tenant_id: uuid.UUID, rule_name: str, rule_id: str, data_source: str, fp_count: int, tp_count: int) -> DetectionMetric:
        
        total = fp_count + tp_count
        status = "HEALTHY"
        
        if total > 0:
            fp_rate = fp_count / total
            if fp_rate > 0.80:
                status = "NOISY"
                
        # In a real scenario we'd check if a rule has stopped firing entirely (BROKEN)
        
        metric = DetectionMetric(
            tenant_id=tenant_id,
            rule_name=rule_name,
            rule_id=rule_id,
            data_source=data_source,
            total_alerts=total,
            false_positives=fp_count,
            true_positives=tp_count,
            status=status,
            last_evaluated_at=datetime.now(timezone.utc)
        )
        
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

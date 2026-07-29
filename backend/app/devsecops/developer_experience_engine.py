import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.devsecops import DeveloperMetric
from app.schemas.devsecops import DeveloperMetricCreate

class DeveloperExperienceEngine:
    """
    Calculates and aggregates developer KPIs, security trends, and guidance.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_developer_metric(self, tenant_id: uuid.UUID, metric_in: DeveloperMetricCreate) -> DeveloperMetric:
        stmt = select(DeveloperMetric).where(
            DeveloperMetric.tenant_id == tenant_id,
            DeveloperMetric.developer_email == metric_in.developer_email
        )
        existing = await self.db.execute(stmt)
        metric = existing.scalar_one_or_none()
        
        if metric:
            metric.code_quality_score = metric_in.code_quality_score
            metric.security_score = metric_in.security_score
            metric.vulnerabilities_introduced = metric_in.vulnerabilities_introduced
            metric.vulnerabilities_fixed = metric_in.vulnerabilities_fixed
            metric.training_completed = metric_in.training_completed
        else:
            metric = DeveloperMetric(
                tenant_id=tenant_id,
                developer_email=metric_in.developer_email,
                code_quality_score=metric_in.code_quality_score,
                security_score=metric_in.security_score,
                vulnerabilities_introduced=metric_in.vulnerabilities_introduced,
                vulnerabilities_fixed=metric_in.vulnerabilities_fixed,
                training_completed=metric_in.training_completed
            )
            self.db.add(metric)
            
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def get_developer_metric(self, tenant_id: uuid.UUID, email: str) -> Optional[DeveloperMetric]:
        stmt = select(DeveloperMetric).where(
            DeveloperMetric.tenant_id == tenant_id,
            DeveloperMetric.developer_email == email
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_top_developers(self, tenant_id: uuid.UUID, limit: int = 10) -> List[DeveloperMetric]:
        stmt = select(DeveloperMetric).where(DeveloperMetric.tenant_id == tenant_id).order_by(DeveloperMetric.security_score.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

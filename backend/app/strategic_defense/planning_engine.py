import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.strategic_defense import OptimizationRoadmap
from datetime import datetime

class StrategicPlanningEngine:
    """
    Constructs multi-phase security roadmaps based on identified gaps.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_roadmap_initiative(self, tenant_id: uuid.UUID, title: str, nist_func: str, start: datetime, end: datetime) -> OptimizationRoadmap:
        roadmap = OptimizationRoadmap(
            tenant_id=tenant_id,
            title=title,
            nist_function=nist_func,
            status="PLANNED",
            start_date=start,
            target_end_date=end
        )
        self.db.add(roadmap)
        await self.db.commit()
        await self.db.refresh(roadmap)
        return roadmap

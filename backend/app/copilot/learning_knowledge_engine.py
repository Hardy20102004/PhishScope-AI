import uuid
from typing import List
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.copilot import DeveloperLearningProgress
from app.schemas.copilot import DeveloperLearningProgressCreate

class LearningKnowledgeEngine:
    """
    Tracks and recommends security training modules based on review findings.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_progress(self, tenant_id: uuid.UUID, developer_id: uuid.UUID, progress_in: DeveloperLearningProgressCreate) -> DeveloperLearningProgress:
        stmt = select(DeveloperLearningProgress).where(
            DeveloperLearningProgress.tenant_id == tenant_id,
            DeveloperLearningProgress.developer_id == developer_id,
            DeveloperLearningProgress.topic == progress_in.topic
        )
        res = await self.db.execute(stmt)
        progress = res.scalar_one_or_none()
        
        if progress:
            progress.modules_completed = progress_in.modules_completed
            progress.last_engaged_at = datetime.now(timezone.utc)
        else:
            progress = DeveloperLearningProgress(
                tenant_id=tenant_id,
                developer_id=developer_id,
                topic=progress_in.topic,
                modules_completed=progress_in.modules_completed
            )
            self.db.add(progress)
            
        await self.db.commit()
        await self.db.refresh(progress)
        return progress

    async def get_learning_profile(self, tenant_id: uuid.UUID, developer_id: uuid.UUID) -> List[DeveloperLearningProgress]:
        stmt = select(DeveloperLearningProgress).where(
            DeveloperLearningProgress.tenant_id == tenant_id,
            DeveloperLearningProgress.developer_id == developer_id
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

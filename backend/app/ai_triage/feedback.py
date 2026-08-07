import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ai_triage import AnalystFeedback

class FeedbackLearningEngine:
    """
    Processes analyst feedback (e.g. False Positive flags, Priority Overrides)
    and stages them for ingestion into the ML training pipeline.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_feedback(
        self, 
        triage_group_id: uuid.UUID, 
        user_id: uuid.UUID, 
        feedback_type: str, 
        comments: str = None
    ) -> AnalystFeedback:
        """
        Logs feedback for continuous learning.
        """
        feedback = AnalystFeedback(
            triage_group_id=triage_group_id,
            user_id=user_id,
            feedback_type=feedback_type,
            comments=comments,
            processed_by_learning_engine=False
        )
        
        self.db.add(feedback)
        await self.db.commit()
        await self.db.refresh(feedback)
        
        return feedback

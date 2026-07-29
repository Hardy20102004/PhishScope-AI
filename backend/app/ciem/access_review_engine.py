import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ciem import AccessReview

class AccessReviewEngine:
    """
    Manages the governance workflow for attesting or revoking access.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_review_campaign(self, tenant_id: uuid.UUID, identity_id: uuid.UUID) -> AccessReview:
        review = AccessReview(
            tenant_id=tenant_id,
            identity_id=identity_id,
            status="PENDING"
        )
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

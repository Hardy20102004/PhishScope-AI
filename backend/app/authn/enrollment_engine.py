import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.authn import AuthnEnrollment

class EnrollmentEngine:
    """
    Governs the creation, activation, recovery, and revocation of authenticators.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_enrollments(self, tenant_id: uuid.UUID) -> List[AuthnEnrollment]:
        result = await self.db.execute(select(AuthnEnrollment).where(AuthnEnrollment.tenant_id == tenant_id))
        return result.scalars().all()

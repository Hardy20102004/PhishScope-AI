import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.executive_intelligence import DecisionSupportBrief
from typing import List

class DecisionSupportEngine:
    """
    Generates structured executive recommendations based on aggregated data.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_executive_brief(self, tenant_id: uuid.UUID, title: str, summary: str, recs: List[str]) -> DecisionSupportBrief:
        brief = DecisionSupportBrief(
            tenant_id=tenant_id,
            title=title,
            executive_summary=summary,
            recommendations=recs
        )
        self.db.add(brief)
        await self.db.commit()
        await self.db.refresh(brief)
        return brief

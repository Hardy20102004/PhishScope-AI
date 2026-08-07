import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.copilot import DeveloperCopilotSession, CopilotSessionStatus
from app.schemas.copilot import DeveloperCopilotSessionCreate

class DeveloperCopilotEngine:
    """
    Manages real-time interaction logic and session context for IDEs.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def initialize_session(self, tenant_id: uuid.UUID, developer_id: uuid.UUID, session_in: DeveloperCopilotSessionCreate) -> DeveloperCopilotSession:
        session = DeveloperCopilotSession(
            tenant_id=tenant_id,
            developer_id=developer_id,
            repository_context=session_in.repository_context,
            environment=session_in.environment,
            status=session_in.status
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def list_active_sessions(self, tenant_id: uuid.UUID, developer_id: uuid.UUID) -> List[DeveloperCopilotSession]:
        stmt = select(DeveloperCopilotSession).where(
            DeveloperCopilotSession.tenant_id == tenant_id,
            DeveloperCopilotSession.developer_id == developer_id,
            DeveloperCopilotSession.status == CopilotSessionStatus.ACTIVE
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

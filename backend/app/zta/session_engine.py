from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.zta import ZTASessionState, SessionStatus, RiskLevel

class SessionIntelligenceEngine:
    """
    Monitors session health, detects anomalies, and manages active sessions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_session(self, tenant_id: uuid.UUID, identity_id: str, device_id: Optional[str] = None) -> ZTASessionState:
        session = ZTASessionState(
            tenant_id=tenant_id,
            session_identifier=f"sess_{uuid.uuid4().hex}",
            identity_id=identity_id,
            device_id=device_id,
            status=SessionStatus.ACTIVE
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_active_sessions(self, tenant_id: uuid.UUID) -> List[ZTASessionState]:
        result = await self.db.execute(
            select(ZTASessionState).where(ZTASessionState.tenant_id == tenant_id, ZTASessionState.status == SessionStatus.ACTIVE)
        )
        return result.scalars().all()

    async def revoke_session(self, session_id: uuid.UUID) -> Optional[ZTASessionState]:
        result = await self.db.execute(select(ZTASessionState).where(ZTASessionState.id == session_id))
        session = result.scalar_one_or_none()
        if session:
            session.status = SessionStatus.REVOKED
            await self.db.commit()
            await self.db.refresh(session)
        return session

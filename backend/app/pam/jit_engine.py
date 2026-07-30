import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pam import PAMJITRequest, JITRequestStatus

class JITAccessEngine:
    """
    Handles Just-in-Time (JIT) access requests, approval routing, and provisioning.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_request(self, tenant_id: uuid.UUID, data: Dict[str, Any]) -> PAMJITRequest:
        req = PAMJITRequest(
            tenant_id=tenant_id,
            requester_id=data["requester_id"],
            target_role=data["target_role"],
            target_resource=data["target_resource"],
            justification=data["justification"],
            ticket_reference=data.get("ticket_reference"),
            requested_duration_minutes=data.get("requested_duration_minutes", 60)
        )
        self.db.add(req)
        await self.db.commit()
        await self.db.refresh(req)
        return req

    async def get_requests(self, tenant_id: uuid.UUID) -> List[PAMJITRequest]:
        result = await self.db.execute(select(PAMJITRequest).where(PAMJITRequest.tenant_id == tenant_id))
        return result.scalars().all()

    async def approve_request(self, request_id: uuid.UUID, approved_by: str, notes: Optional[str] = None) -> Optional[PAMJITRequest]:
        result = await self.db.execute(select(PAMJITRequest).where(PAMJITRequest.id == request_id))
        req = result.scalar_one_or_none()
        if req and req.status == JITRequestStatus.PENDING_APPROVAL:
            req.status = JITRequestStatus.APPROVED
            req.approved_by = approved_by
            req.approval_notes = notes
            # Automatically activate for simulation
            req.status = JITRequestStatus.ACTIVE
            req.activated_at = datetime.now(timezone.utc)
            req.expires_at = req.activated_at + timedelta(minutes=req.requested_duration_minutes)
            await self.db.commit()
            await self.db.refresh(req)
        return req

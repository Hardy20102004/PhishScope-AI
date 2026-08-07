from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.zta import ZTAPolicyApproval

class PolicyGovernanceEngine:
    """
    Handles policy lifecycles and human approval workflows.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_approval_request(self, tenant_id: uuid.UUID, policy_id: uuid.UUID, data: Dict[str, Any]) -> ZTAPolicyApproval:
        approval = ZTAPolicyApproval(
            tenant_id=tenant_id,
            policy_id=policy_id,
            requested_by=data["requested_by"],
            requested_changes=data.get("requested_changes", {}),
            justification=data["justification"]
        )
        self.db.add(approval)
        await self.db.commit()
        await self.db.refresh(approval)
        return approval

    async def get_pending_approvals(self, tenant_id: uuid.UUID) -> List[ZTAPolicyApproval]:
        result = await self.db.execute(
            select(ZTAPolicyApproval).where(ZTAPolicyApproval.tenant_id == tenant_id, ZTAPolicyApproval.status == "PENDING")
        )
        return result.scalars().all()

    async def resolve_approval(self, approval_id: uuid.UUID, approved_by: str, status: str) -> Optional[ZTAPolicyApproval]:
        result = await self.db.execute(select(ZTAPolicyApproval).where(ZTAPolicyApproval.id == approval_id))
        approval = result.scalar_one_or_none()
        if approval:
            approval.status = status
            approval.approved_by = approved_by
            approval.resolved_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(approval)
        return approval

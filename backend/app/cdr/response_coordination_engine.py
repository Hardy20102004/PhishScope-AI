import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cdr import ResponseAction, CloudInvestigation

class ResponseCoordinationEngine:
    """
    Generates playbook recommendations for active investigations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def propose_containment(self, investigation: CloudInvestigation) -> ResponseAction:
        action = ResponseAction(
            tenant_id=investigation.tenant_id,
            investigation_id=investigation.id,
            action_type="REVOKE_IAM_SESSIONS",
            target_entity=investigation.primary_entity,
            description=f"Automatically revoke all active cloud sessions for principal {investigation.primary_entity}."
        )
        self.db.add(action)
        await self.db.commit()
        await self.db.refresh(action)
        return action

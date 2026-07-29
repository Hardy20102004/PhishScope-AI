import uuid
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.iac import IaCDeploymentGovernance, IaCDeploymentStatus
from app.schemas.iac import IaCDeploymentGovernanceCreate

class DeploymentGovernanceEngine:
    """
    Orchestrates pre-deployment gate logic (Approval Workflows).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def request_deployment(self, tenant_id: uuid.UUID, deployment_in: IaCDeploymentGovernanceCreate) -> IaCDeploymentGovernance:
        deployment = IaCDeploymentGovernance(
            tenant_id=tenant_id,
            template_id=deployment_in.template_id,
            status=deployment_in.status,
            requested_by=deployment_in.requested_by,
            risk_score=deployment_in.risk_score
        )
        self.db.add(deployment)
        await self.db.commit()
        await self.db.refresh(deployment)
        return deployment

    async def approve_deployment(self, tenant_id: uuid.UUID, deployment_id: uuid.UUID, approved_by: uuid.UUID) -> Optional[IaCDeploymentGovernance]:
        stmt = select(IaCDeploymentGovernance).where(
            IaCDeploymentGovernance.id == deployment_id,
            IaCDeploymentGovernance.tenant_id == tenant_id
        )
        res = await self.db.execute(stmt)
        deployment = res.scalar_one_or_none()
        
        if deployment:
            deployment.status = IaCDeploymentStatus.APPROVED
            deployment.approved_by = approved_by
            deployment.resolved_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(deployment)
            
        return deployment

    async def list_deployments(self, tenant_id: uuid.UUID) -> List[IaCDeploymentGovernance]:
        stmt = select(IaCDeploymentGovernance).where(IaCDeploymentGovernance.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

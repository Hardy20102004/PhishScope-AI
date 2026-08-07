import uuid
from typing import List
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.appsec_command_center import AppSecExecutiveMetric, AppSecGovernanceDecision, GovernanceDecisionStatus
from app.schemas.appsec_command_center import AppSecExecutiveMetricCreate, AppSecGovernanceDecisionCreate

class ExecutiveDecisionSupportEngine:
    """
    Processes metrics for board reporting and orchestrates governance approvals.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_executive_metric(self, tenant_id: uuid.UUID, metric_in: AppSecExecutiveMetricCreate) -> AppSecExecutiveMetric:
        metric = AppSecExecutiveMetric(
            tenant_id=tenant_id,
            enterprise_risk_score=metric_in.enterprise_risk_score,
            compliance_posture=metric_in.compliance_posture,
            total_critical_vulnerabilities=metric_in.total_critical_vulnerabilities
        )
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def get_executive_metrics(self, tenant_id: uuid.UUID) -> List[AppSecExecutiveMetric]:
        stmt = select(AppSecExecutiveMetric).where(AppSecExecutiveMetric.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def propose_governance_decision(self, tenant_id: uuid.UUID, requested_by: uuid.UUID, decision_in: AppSecGovernanceDecisionCreate) -> AppSecGovernanceDecision:
        decision = AppSecGovernanceDecision(
            tenant_id=tenant_id,
            policy_name=decision_in.policy_name,
            proposed_change=decision_in.proposed_change,
            status=GovernanceDecisionStatus.PENDING,
            requested_by=requested_by
        )
        self.db.add(decision)
        await self.db.commit()
        await self.db.refresh(decision)
        return decision

    async def approve_governance_decision(self, tenant_id: uuid.UUID, decision_id: uuid.UUID, approved_by: uuid.UUID) -> AppSecGovernanceDecision:
        stmt = select(AppSecGovernanceDecision).where(
            AppSecGovernanceDecision.id == decision_id,
            AppSecGovernanceDecision.tenant_id == tenant_id
        )
        res = await self.db.execute(stmt)
        decision = res.scalar_one_or_none()
        if decision:
            decision.status = GovernanceDecisionStatus.APPROVED
            decision.approved_by = approved_by
            decision.resolved_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(decision)
        return decision

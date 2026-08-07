import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.blue_team import AnalystTeamMetric

class AnalystReadinessEngine:
    """
    Calculates operational efficiency metrics for SOC tiers.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_team_metrics(self, tenant_id: uuid.UUID, team_name: str, period: str, mtt: float, mttr: float, adherence: float) -> AnalystTeamMetric:
        
        metric = AnalystTeamMetric(
            tenant_id=tenant_id,
            team_name=team_name,
            evaluation_period=period,
            mean_time_to_triage_mins=mtt,
            mean_time_to_resolve_mins=mttr,
            playbook_adherence_percent=adherence
        )
        
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

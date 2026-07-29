import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.devsecops import PipelineRun
from app.schemas.devsecops import PipelineRunCreate

class PipelineIntegrationEngine:
    """
    Ingests and normalizes pipeline events from external CI/CD systems (GitHub Actions, GitLab CI, etc.).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_pipeline_run(self, tenant_id: uuid.UUID, run_in: PipelineRunCreate) -> PipelineRun:
        run = PipelineRun(
            tenant_id=tenant_id,
            repository_id=run_in.repository_id,
            application_id=run_in.application_id,
            ci_provider=run_in.ci_provider,
            run_identifier=run_in.run_identifier,
            branch=run_in.branch,
            commit_sha=run_in.commit_sha,
            status=run_in.status,
            sdlc_phase=run_in.sdlc_phase,
            triggered_by=run_in.triggered_by,
            started_at=run_in.started_at,
            completed_at=run_in.completed_at
        )
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        return run

    async def get_pipeline_run(self, run_id: uuid.UUID) -> Optional[PipelineRun]:
        stmt = select(PipelineRun).where(PipelineRun.id == run_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_pipeline_runs(self, tenant_id: uuid.UUID) -> List[PipelineRun]:
        stmt = select(PipelineRun).where(PipelineRun.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

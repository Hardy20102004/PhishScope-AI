import uuid
import structlog
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.aspm import CodeRepository
from app.schemas.aspm import CodeRepositoryCreate

logger = structlog.get_logger("phoenix.aspm.repository")

class RepositoryIntegrationEngine:
    """
    Manages connections to SCM providers (GitHub, GitLab, Bitbucket).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_repository(self, tenant_id: uuid.UUID, repo_in: CodeRepositoryCreate) -> CodeRepository:
        stmt = select(CodeRepository).where(
            CodeRepository.tenant_id == tenant_id,
            CodeRepository.url == repo_in.url
        )
        existing = await self.db.execute(stmt)
        repo = existing.scalar_one_or_none()
        
        if repo:
            repo.name = repo_in.name
            repo.provider = repo_in.provider
            repo.default_branch = repo_in.default_branch
            repo.is_active = repo_in.is_active
            if repo_in.application_id:
                repo.application_id = repo_in.application_id
        else:
            repo = CodeRepository(
                tenant_id=tenant_id,
                application_id=repo_in.application_id,
                name=repo_in.name,
                url=repo_in.url,
                provider=repo_in.provider,
                default_branch=repo_in.default_branch,
                is_active=repo_in.is_active
            )
            self.db.add(repo)
            
        await self.db.commit()
        await self.db.refresh(repo)
        return repo

    async def list_repositories(self, tenant_id: uuid.UUID) -> List[CodeRepository]:
        stmt = select(CodeRepository).where(CodeRepository.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def sync_repository_metadata(self, repo_id: uuid.UUID) -> None:
        """
        Simulates fetching branches, commits, and dependencies from SCM.
        """
        logger.info("syncing_repository", repository_id=str(repo_id))
        stmt = select(CodeRepository).where(CodeRepository.id == repo_id)
        res = await self.db.execute(stmt)
        repo = res.scalar_one_or_none()
        if repo:
            # Simulate a successful sync by updating the last_scanned timestamp
            from datetime import datetime, timezone
            repo.last_scanned = datetime.now(timezone.utc)
            await self.db.commit()

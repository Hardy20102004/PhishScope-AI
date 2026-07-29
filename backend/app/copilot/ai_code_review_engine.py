import uuid
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.copilot import CodeReviewRecord, CodeReviewFinding, CodeReviewStatus
from app.schemas.copilot import CodeReviewRecordCreate, CodeReviewFindingCreate

class AICodeReviewEngine:
    """
    Analyzes code snippets or PRs for security patterns.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_review(self, tenant_id: uuid.UUID, review_in: CodeReviewRecordCreate) -> CodeReviewRecord:
        review = CodeReviewRecord(
            tenant_id=tenant_id,
            repository_url=review_in.repository_url,
            pull_request_id=review_in.pull_request_id,
            commit_hash=review_in.commit_hash,
            status=CodeReviewStatus.COMPLETED # Auto-completing for mock
        )
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def add_finding(self, tenant_id: uuid.UUID, finding_in: CodeReviewFindingCreate) -> CodeReviewFinding:
        finding = CodeReviewFinding(
            tenant_id=tenant_id,
            review_id=finding_in.review_id,
            file_path=finding_in.file_path,
            line_number=finding_in.line_number,
            severity=finding_in.severity,
            cwe_id=finding_in.cwe_id,
            description=finding_in.description,
            suggestion=finding_in.suggestion
        )
        self.db.add(finding)
        
        # Update finding count on review record
        stmt = select(CodeReviewRecord).where(CodeReviewRecord.id == finding_in.review_id)
        review = (await self.db.execute(stmt)).scalar_one_or_none()
        if review:
            review.findings_count += 1
            
        await self.db.commit()
        await self.db.refresh(finding)
        return finding

    async def list_reviews(self, tenant_id: uuid.UUID) -> List[CodeReviewRecord]:
        stmt = select(CodeReviewRecord).where(CodeReviewRecord.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

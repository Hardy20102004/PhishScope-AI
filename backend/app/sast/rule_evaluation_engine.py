import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sast import SASTRule
from app.schemas.sast import SASTRuleCreate

class RuleEvaluationEngine:
    """
    Evaluates static analysis rules and patterns against the source code syntax.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_rule(self, tenant_id: uuid.UUID, rule_in: SASTRuleCreate) -> SASTRule:
        rule = SASTRule(
            tenant_id=tenant_id,
            rule_id=rule_in.rule_id,
            name=rule_in.name,
            description=rule_in.description,
            cwe=rule_in.cwe,
            owasp_category=rule_in.owasp_category,
            severity=rule_in.severity
        )
        self.db.add(rule)
        await self.db.commit()
        await self.db.refresh(rule)
        return rule

    async def list_rules(self, tenant_id: uuid.UUID) -> List[SASTRule]:
        stmt = select(SASTRule).where(SASTRule.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

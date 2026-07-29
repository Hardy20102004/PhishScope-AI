import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.detection import DetectionRule, RuleApprovalRecord, DetectionRuleVersion, RuleTestResult

class RuleApprovalWorkflow:
    """
    Enforces strict state transitions for the detection engineering lifecycle.
    """
    
    VALID_TRANSITIONS = {
        "DRAFT": ["IN_REVIEW", "RETIRED"],
        "IN_REVIEW": ["APPROVED", "DRAFT", "RETIRED"],
        "APPROVED": ["READY_FOR_DEPLOYMENT", "DRAFT"],
        "READY_FOR_DEPLOYMENT": ["DEPLOYED", "DRAFT"],
        "DEPLOYED": ["RETIRED"],
        "RETIRED": ["DRAFT"]
    }
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def transition_status(
        self, 
        rule_id: uuid.UUID, 
        new_status: str, 
        user_id: uuid.UUID, 
        notes: Optional[str] = None
    ) -> DetectionRule:
        """
        Attempts to transition a rule to a new status.
        Enforces testing requirements before approval.
        """
        result = await self.db.execute(select(DetectionRule).where(DetectionRule.id == rule_id))
        rule = result.scalar_one_or_none()
        if not rule:
            raise ValueError("Rule not found")
            
        current_status = rule.status
        
        if new_status not in self.VALID_TRANSITIONS.get(current_status, []):
            raise ValueError(f"Invalid transition from {current_status} to {new_status}")
            
        # Business Logic: Cannot approve without passing tests
        if new_status == "APPROVED":
            # Fetch latest version
            version_result = await self.db.execute(
                select(DetectionRuleVersion).where(
                    DetectionRuleVersion.rule_id == rule.id,
                    DetectionRuleVersion.version == rule.current_version
                )
            )
            latest_version = version_result.scalar_one_or_none()
            
            if latest_version:
                test_result = await self.db.execute(
                    select(RuleTestResult).where(RuleTestResult.version_id == latest_version.id)
                )
                tests = test_result.scalars().all()
                if not tests or not any(t.passed for t in tests):
                    raise ValueError("Cannot approve a rule that has not passed regression testing.")
                    
        # Apply transition
        rule.status = new_status
        
        # Audit Log
        if latest_version := await self._get_latest_version(rule.id, rule.current_version):
            record = RuleApprovalRecord(
                rule_id=rule.id,
                version_id=latest_version.id,
                approver_id=user_id,
                status_changed_to=new_status,
                notes=notes
            )
            self.db.add(record)
            
        await self.db.commit()
        await self.db.refresh(rule)
        return rule

    async def _get_latest_version(self, rule_id: uuid.UUID, version: int):
        result = await self.db.execute(
            select(DetectionRuleVersion).where(
                DetectionRuleVersion.rule_id == rule_id,
                DetectionRuleVersion.version == version
            )
        )
        return result.scalar_one_or_none()

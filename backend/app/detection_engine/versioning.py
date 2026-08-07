import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.detection import DetectionRule, DetectionRuleVersion

class RuleVersionManager:
    """
    Manages versions of detection rules.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_new_version(
        self, 
        rule: DetectionRule, 
        new_payload: str, 
        author_id: Optional[uuid.UUID],
        change_summary: Optional[str] = None
    ) -> DetectionRuleVersion:
        """
        Increments the rule version and stores the new payload.
        """
        # Increment parent rule version
        rule.current_version += 1
        
        # Create version record
        version = DetectionRuleVersion(
            rule_id=rule.id,
            version=rule.current_version,
            payload=new_payload,
            change_summary=change_summary,
            author_id=author_id
        )
        
        self.db.add(version)
        # Re-draft the rule when a new version is created if it was approved
        if rule.status in ["APPROVED", "READY_FOR_DEPLOYMENT", "DEPLOYED"]:
            rule.status = "DRAFT"
            
        await self.db.commit()
        await self.db.refresh(version)
        
        return version

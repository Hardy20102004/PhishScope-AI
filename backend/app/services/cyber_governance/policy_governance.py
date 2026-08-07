from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.cyber_governance import GovernancePolicy, PolicyStatus
from app.schemas.cyber_governance import GovernancePolicyCreate

class PolicyGovernanceEngine:
    def __init__(self, db: Session):
        self.db = db

    def create_policy(self, policy_in: GovernancePolicyCreate) -> GovernancePolicy:
        db_policy = GovernancePolicy(
            name=policy_in.name,
            description=policy_in.description,
            version=policy_in.version,
            framework=policy_in.framework,
            status=PolicyStatus.DRAFT
        )
        self.db.add(db_policy)
        self.db.commit()
        self.db.refresh(db_policy)
        return db_policy

    def get_policies(self, skip: int = 0, limit: int = 100) -> List[GovernancePolicy]:
        return self.db.query(GovernancePolicy).offset(skip).limit(limit).all()

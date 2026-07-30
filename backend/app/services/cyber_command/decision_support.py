from typing import List
from sqlalchemy.orm import Session
from app.models.cyber_command import StrategicPlan
from app.schemas.cyber_command import StrategicPlanCreate

class DecisionSupportEngine:
    def __init__(self, db: Session):
        self.db = db

    def create_plan(self, plan_in: StrategicPlanCreate) -> StrategicPlan:
        db_plan = StrategicPlan(
            title=plan_in.title,
            description=plan_in.description,
            horizon=plan_in.horizon,
            milestones=plan_in.milestones,
            budget_allocation=plan_in.budget_allocation
        )
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    def get_plans(self, skip: int = 0, limit: int = 100) -> List[StrategicPlan]:
        return self.db.query(StrategicPlan).offset(skip).limit(limit).all()

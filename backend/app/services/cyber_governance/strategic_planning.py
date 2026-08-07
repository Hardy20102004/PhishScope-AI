from sqlalchemy.orm import Session

class StrategicPlanningEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_investment_priorities(self):
        # Mock logic
        return [
            {"domain": "Identity Security", "priority": "HIGH", "budget_status": "ON_TRACK"},
            {"domain": "Cloud Security", "priority": "HIGH", "budget_status": "AT_RISK"}
        ]

from sqlalchemy.orm import Session

from app.services.cyber_command.enterprise_kpi import EnterpriseKPIEngine
from app.services.cyber_command.coordination import StrategicCoordinationEngine
from app.services.cyber_command.decision_support import DecisionSupportEngine

class CyberCommandManager:
    """
    Central apex orchestrator for the Enterprise Cyber Command Platform.
    Aggregates data across the entire PHOENIX X ecosystem.
    """
    def __init__(self, db: Session):
        self.db = db
        self.kpi = EnterpriseKPIEngine(db)
        self.coordination = StrategicCoordinationEngine(db)
        self.decision = DecisionSupportEngine(db)

    def get_overview_stats(self) -> dict:
        ops = self.coordination.get_active_operations()
        plans = self.decision.get_plans()
        
        return {
            "global_health_score": 92.5,
            "active_operations_count": len(ops),
            "critical_alerts": sum(1 for op in ops if op.get("criticality") == "HIGH"),
            "strategic_alignment_score": 88.0,
            "ai_strategic_briefing": "Enterprise posture is stable. 1 High-criticality SOC operation requires attention."
        }

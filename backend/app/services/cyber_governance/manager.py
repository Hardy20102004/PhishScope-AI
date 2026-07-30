from sqlalchemy.orm import Session

from app.services.cyber_governance.executive_kpi import ExecutiveKPIEngine
from app.services.cyber_governance.policy_governance import PolicyGovernanceEngine
from app.services.cyber_governance.risk_oversight import RiskOversightEngine
from app.services.cyber_governance.board_reporting import BoardReportingEngine
from app.services.cyber_governance.strategic_planning import StrategicPlanningEngine

class CyberGovernanceManager:
    """
    Central orchestrator for the Cyber Governance Platform.
    """
    def __init__(self, db: Session):
        self.db = db
        self.kpi = ExecutiveKPIEngine(db)
        self.policy = PolicyGovernanceEngine(db)
        self.risk = RiskOversightEngine(db)
        self.board = BoardReportingEngine(db)
        self.strategy = StrategicPlanningEngine(db)

    def get_overview_stats(self) -> dict:
        policies = self.policy.get_policies()
        reports = self.board.get_reports()
        
        return {
            "overall_maturity_score": 4.2,
            "active_policies_count": len(policies),
            "critical_risks_count": 3,
            "board_reports_generated": len(reports)
        }

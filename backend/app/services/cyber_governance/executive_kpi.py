from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.cyber_governance import CyberGovernanceKPI
from app.schemas.cyber_governance import CyberGovernanceKPICreate

class ExecutiveKPIEngine:
    def __init__(self, db: Session):
        self.db = db

    def record_kpi(self, kpi_in: CyberGovernanceKPICreate) -> CyberGovernanceKPI:
        db_kpi = CyberGovernanceKPI(
            metric_name=kpi_in.metric_name,
            metric_value=kpi_in.metric_value,
            target_value=kpi_in.target_value,
            category=kpi_in.category
        )
        self.db.add(db_kpi)
        self.db.commit()
        self.db.refresh(db_kpi)
        return db_kpi

    def get_kpis(self, skip: int = 0, limit: int = 100) -> List[CyberGovernanceKPI]:
        return self.db.query(CyberGovernanceKPI).offset(skip).limit(limit).all()

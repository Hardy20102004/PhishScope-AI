from typing import List
from sqlalchemy.orm import Session
from app.models.cyber_governance import BoardReportSummary
from app.schemas.cyber_governance import BoardReportSummaryCreate

class BoardReportingEngine:
    def __init__(self, db: Session):
        self.db = db

    def generate_report(self, report_in: BoardReportSummaryCreate) -> BoardReportSummary:
        db_report = BoardReportSummary(
            title=report_in.title,
            quarter=report_in.quarter,
            summary_text=report_in.summary_text,
            investment_summary=report_in.investment_summary,
            risk_summary=report_in.risk_summary,
            generated_by_ai=report_in.generated_by_ai
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def get_reports(self, skip: int = 0, limit: int = 100) -> List[BoardReportSummary]:
        return self.db.query(BoardReportSummary).offset(skip).limit(limit).all()

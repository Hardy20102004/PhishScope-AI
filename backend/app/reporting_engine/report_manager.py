import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reporting_engine import ForensicReport, ReportSection

class ReportManager:
    """
    Orchestrates the creation and assembly of forensic reports.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def initialize_report(self, tenant_id: uuid.UUID, title: str, report_type: str, author_id: str, inv_id: uuid.UUID = None) -> ForensicReport:
        report = ForensicReport(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            title=title,
            report_type=report_type,
            author_id=author_id
        )
        self.db.add(report)
        await self.db.flush()
        
        # Scaffold default sections
        s1 = ReportSection(report_id=report.id, section_type="EXECUTIVE_SUMMARY", order_index=0, content="Summary of findings...")
        s2 = ReportSection(report_id=report.id, section_type="OBSERVED_EVIDENCE", order_index=1, content="Raw evidence artifacts...")
        s3 = ReportSection(report_id=report.id, section_type="ANALYTICAL_ASSESSMENT", order_index=2, content="Correlations and interpretations...")
        
        self.db.add_all([s1, s2, s3])
        
        await self.db.commit()
        await self.db.refresh(report, ["sections"])
        return report

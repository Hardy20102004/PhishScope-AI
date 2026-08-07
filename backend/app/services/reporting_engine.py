import json
import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reporting import Report, ReportStatus, ReportTemplate
from app.schemas.reporting import ReportCreate, ReportUpdate


class ReportingEngine:
    def __init__(self, db: Session):
        self.db = db
        
    def create_report(self, request: ReportCreate, user_id: uuid.UUID) -> Report:
        # Render HTML from template logic (stubbed for now)
        html_content = ""
        if request.template_id:
            stmt = select(ReportTemplate).where(ReportTemplate.id == request.template_id)
            template = self.db.execute(stmt).scalar_one_or_none()
            if template:
                # Basic substitution
                html_content = template.html_template
                for k, v in request.content_data.items():
                    html_content = html_content.replace(f"{{{{{k}}}}}", str(v))
        else:
            html_content = f"<h1>{request.title}</h1><pre>{json.dumps(request.content_data, indent=2)}</pre>"
            
        report = Report(
            title=request.title,
            case_id=request.case_id,
            investigation_id=request.investigation_id,
            template_id=request.template_id,
            content_data=request.content_data,
            rendered_html=html_content,
            created_by=user_id
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_report(self, report_id: uuid.UUID) -> Report:
        stmt = select(Report).where(Report.id == report_id)
        report = self.db.execute(stmt).scalar_one_or_none()
        if not report:
            raise ValueError("Report not found")
        return report
        
    def list_reports(self, case_id: Optional[uuid.UUID] = None) -> List[Report]:
        stmt = select(Report)
        if case_id:
            stmt = stmt.where(Report.case_id == case_id)
        stmt = stmt.order_by(Report.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())

    def update_report(self, report_id: uuid.UUID, request: ReportUpdate, user_id: uuid.UUID) -> Report:
        report = self.get_report(report_id)
        
        if request.title is not None:
            report.title = request.title
        if request.content_data is not None:
            report.content_data = request.content_data
            # Re-render HTML logic here...
            
        if request.status is not None:
            report.status = request.status
            if request.status == ReportStatus.APPROVED:
                report.approved_by = user_id
                
        self.db.commit()
        self.db.refresh(report)
        return report

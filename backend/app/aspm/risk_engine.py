import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.aspm import EnterpriseApplication, SecurityFinding, ApplicationRisk

class ApplicationRiskEngine:
    """
    Evaluates finding density, business criticality, and exposure to compute an overall Application Risk Score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_risk(self, app_id: uuid.UUID) -> ApplicationRisk:
        # Fetch App
        app_stmt = select(EnterpriseApplication).where(EnterpriseApplication.id == app_id)
        app = (await self.db.execute(app_stmt)).scalar_one_or_none()
        if not app:
            raise ValueError(f"Application {app_id} not found.")

        # Fetch Findings
        find_stmt = select(SecurityFinding).where(
            SecurityFinding.application_id == app_id,
            SecurityFinding.status == "OPEN"
        )
        findings = (await self.db.execute(find_stmt)).scalars().all()
        
        crit_count = sum(1 for f in findings if f.severity.value == "CRITICAL")
        high_count = sum(1 for f in findings if f.severity.value == "HIGH")
        
        # Simple weighted risk scoring model
        base_score = (crit_count * 10) + (high_count * 5)
        
        # Adjust for criticality
        if app.criticality.value == "CRITICAL":
            base_score *= 1.5
        elif app.criticality.value == "HIGH":
            base_score *= 1.2
            
        # Adjust for internet exposure
        if app.is_internet_facing:
            base_score *= 1.3
            
        final_score = min(base_score, 100.0)
        
        # Update or Create Risk Record
        risk_stmt = select(ApplicationRisk).where(ApplicationRisk.application_id == app_id)
        risk = (await self.db.execute(risk_stmt)).scalar_one_or_none()
        
        if risk:
            risk.overall_risk_score = final_score
            risk.critical_findings_count = crit_count
            risk.high_findings_count = high_count
        else:
            risk = ApplicationRisk(
                tenant_id=app.tenant_id,
                application_id=app_id,
                overall_risk_score=final_score,
                critical_findings_count=crit_count,
                high_findings_count=high_count
            )
            self.db.add(risk)
            
        await self.db.commit()
        await self.db.refresh(risk)
        return risk

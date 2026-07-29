import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sca import SCARiskScore, SCARiskLevel
from app.schemas.sca import SCARiskScoreCreate

class SupplyChainRiskEngine:
    """
    Generates the composite SCARiskScore for each dependency based on vulnerabilities, license risk, and maintainer activity.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_risk(self, tenant_id: uuid.UUID, score_in: SCARiskScoreCreate) -> SCARiskScore:
        overall_score = (score_in.vulnerability_risk * 0.5) + (score_in.license_risk * 0.3) + (score_in.operational_risk * 0.2)
        
        risk_level = SCARiskLevel.INFO
        if overall_score > 80:
            risk_level = SCARiskLevel.CRITICAL
        elif overall_score > 60:
            risk_level = SCARiskLevel.HIGH
        elif overall_score > 40:
            risk_level = SCARiskLevel.MEDIUM
        elif overall_score > 20:
            risk_level = SCARiskLevel.LOW
            
        score = SCARiskScore(
            tenant_id=tenant_id,
            dependency_id=score_in.dependency_id,
            vulnerability_risk=score_in.vulnerability_risk,
            license_risk=score_in.license_risk,
            operational_risk=score_in.operational_risk,
            overall_score=overall_score,
            risk_level=risk_level
        )
        self.db.add(score)
        await self.db.commit()
        await self.db.refresh(score)
        return score

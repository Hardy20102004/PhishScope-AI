from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.zta import ZTARiskEvaluation, RiskLevel

class RiskDecisionEngine:
    """
    Quantifies contextual risk.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def evaluate_risk(self, tenant_id: uuid.UUID, context_snapshot_id: uuid.UUID, context_data: Dict[str, Any]) -> ZTARiskEvaluation:
        # Simulated risk logic
        identity_risk = 20.0
        device_risk = 15.0
        session_risk = 10.0
        app_risk = 25.0
        
        # Simple weighted sum
        composite = (identity_risk * 0.3) + (device_risk * 0.3) + (session_risk * 0.2) + (app_risk * 0.2)
        
        level = RiskLevel.LOW
        if composite > 75:
            level = RiskLevel.CRITICAL
        elif composite > 50:
            level = RiskLevel.HIGH
        elif composite > 25:
            level = RiskLevel.MEDIUM

        factors = []
        if app_risk > 20:
            factors.append("High criticality application requested.")
        if device_risk > 10:
            factors.append("Device trust is not optimal.")

        evaluation = ZTARiskEvaluation(
            tenant_id=tenant_id,
            context_snapshot_id=context_snapshot_id,
            identity_risk_score=identity_risk,
            device_risk_score=device_risk,
            session_risk_score=session_risk,
            app_risk_score=app_risk,
            composite_risk_score=composite,
            risk_level=level,
            contributing_factors=factors,
            confidence=0.85
        )
        self.db.add(evaluation)
        await self.db.commit()
        await self.db.refresh(evaluation)
        return evaluation

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ai_triage import AITriageGroup
from app.ai_triage.grouping import AlertGroupingEngine
from app.ai_triage.business_impact import BusinessImpactEngine
from app.ai_triage.priority import PriorityEngine
from app.ai_triage.recommendation import RecommendationEngine

class AITriageManager:
    """
    Central orchestrator for the AI Triage Platform.
    Groups incoming alerts, calculates their business impact, sets an advanced priority score,
    and generates AI-backed recommendations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.grouping_engine = AlertGroupingEngine(db)
        self.impact_engine = BusinessImpactEngine(db)
        self.priority_engine = PriorityEngine(db)
        self.recommendation_engine = RecommendationEngine(db)

    async def triage_alert_batch(self, alert_ids: list[uuid.UUID], tenant_id: uuid.UUID) -> AITriageGroup:
        """
        Takes a raw batch of alerts and processes them through the full AI triage pipeline.
        """
        # 1. Grouping
        triage_group = await self.grouping_engine.group_alerts(alert_ids, tenant_id)
        
        # 2. Extract context to find target assets
        # (Mocking asset extraction - assume we found IP 10.0.0.5)
        asset_identifier = "10.0.0.5"
        
        # 3. Business Impact
        impact_score = await self.impact_engine.calculate_impact(asset_identifier, tenant_id)
        triage_group.business_impact_score = impact_score
        
        # 4. Priority Score
        # Assume average threat severity of the alerts is 70 for this example
        base_threat_severity = 70.0 
        priority_result = await self.priority_engine.calculate_priority(
            base_threat_severity=base_threat_severity,
            business_impact_score=impact_score,
            confidence_multiplier=triage_group.confidence
        )
        triage_group.overall_priority_score = priority_result["score"]
        triage_group.priority_tier = priority_result["tier"]
        
        await self.db.commit()
        
        # 5. Generate Recommendation
        await self.recommendation_engine.generate_recommendation(triage_group.id)
        
        return triage_group

import pytest
import uuid
from datetime import datetime, timezone, timedelta
from app.strategic_defense.forecasting_engine import ForecastingEngine
from app.strategic_defense.planning_engine import StrategicPlanningEngine
from app.strategic_defense.optimization_engine import OptimizationEngine
from app.strategic_defense.decision_support_engine import DecisionSupportEngine
from app.models.strategic_defense import StrategicRecommendation

pytestmark = pytest.mark.asyncio

async def test_strategic_defense_workflows(db_session):
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    # 1. Test Forecasting
    fe = ForecastingEngine(db_session)
    future_date = datetime.now(timezone.utc) + timedelta(days=365)
    forecast = await fe.generate_forecast(tenant_id, "OVERALL_RESILIENCE", future_date, 92.0, 0.94)
    
    assert forecast.metric_name == "OVERALL_RESILIENCE"
    assert forecast.projected_value == 92.0
    
    # 2. Test Roadmap Planning
    spe = StrategicPlanningEngine(db_session)
    start = datetime.now(timezone.utc)
    end = start + timedelta(days=90)
    roadmap = await spe.add_roadmap_initiative(tenant_id, "Zero Trust Rollout", "PROTECT", start, end)
    
    assert roadmap.nist_function == "PROTECT"
    assert roadmap.status == "PLANNED"
    
    # 3. Test Optimization & Human Approval Workflow
    oe = OptimizationEngine(db_session)
    rec = await oe.generate_recommendation(tenant_id, "Consolidate EDR", "Overlap detected.", "$450k savings")
    
    assert rec.status == "PENDING_REVIEW"
    
    dse = DecisionSupportEngine(db_session)
    log = await dse.record_decision(tenant_id, rec.id, user_id, "APPROVED", "Fits FY26 budget.")
    
    # Refresh rec to check status
    updated_rec = await db_session.get(StrategicRecommendation, rec.id)
    
    assert updated_rec.status == "APPROVED"
    assert log.action_taken == "APPROVED"
    assert log.justification == "Fits FY26 budget."

import pytest
import uuid
from app.executive_intelligence.business_impact_engine import BusinessImpactEngine
from app.executive_intelligence.investment_engine import InvestmentAnalyticsEngine
from app.executive_intelligence.decision_support_engine import DecisionSupportEngine

pytestmark = pytest.mark.asyncio

async def test_executive_intelligence(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Business Impact
    bie = BusinessImpactEngine(db_session)
    impact = await bie.assess_service_impact(tenant_id, "Payments API", "MISSION_CRITICAL", 88.0, "AT_RISK")
    
    assert impact.service_name == "Payments API"
    assert impact.criticality == "MISSION_CRITICAL"
    
    # 2. Test Investment ROI
    iae = InvestmentAnalyticsEngine(db_session)
    roi = await iae.log_investment_roi(tenant_id, "SOAR Automation", "ACTIVE", 420.0, 15.0)
    
    assert roi.hours_saved_monthly == 420.0
    assert roi.risk_reduction_percentage == 15.0
    
    # 3. Test Decision Support Brief
    dse = DecisionSupportEngine(db_session)
    brief = await dse.generate_executive_brief(tenant_id, "Modernize API", "High risk on API.", ["Enforce OAuth2"])
    
    assert brief.title == "Modernize API"
    assert "Enforce OAuth2" in brief.recommendations

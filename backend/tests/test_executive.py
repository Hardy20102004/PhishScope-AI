import pytest
import uuid

from app.executive.analytics_engine import AnalyticsEngine
from app.executive.risk_engine import RiskEngine
from app.executive.ai_executive_assistant import AIExecutiveAssistant

pytestmark = pytest.mark.asyncio

async def test_analytics_kpi_engine(db_session):
    tenant_id = uuid.uuid4()
    
    engine = AnalyticsEngine(db_session)
    kpis = await engine.get_kpis(tenant_id)
    
    assert "mttr_hours" in kpis
    assert "mtta_mins" in kpis
    assert kpis["mttr_hours"] > 0

async def test_business_risk_engine(db_session):
    tenant_id = uuid.uuid4()
    
    engine = RiskEngine(db_session)
    risks = await engine.calculate_business_risk(tenant_id)
    
    assert len(risks) > 0
    finance_risk = next(r for r in risks if r["business_unit"] == "Finance")
    assert finance_risk["status"] == "HIGH"

async def test_ai_board_report(db_session):
    tenant_id = uuid.uuid4()
    
    assistant = AIExecutiveAssistant(db_session)
    report = await assistant.generate_board_report(tenant_id)
    
    assert report.id is not None
    assert report.report_type == "MONTHLY_BOARD_REPORT"
    assert "CISO Board Report" in report.content

import pytest
import uuid

from app.models.ai_triage import AssetBusinessContext
from app.ai_triage.business_impact import BusinessImpactEngine
from app.ai_triage.priority import PriorityEngine
from app.ai_triage.triage_manager import AITriageManager

pytestmark = pytest.mark.asyncio

async def test_business_impact_calculation(db_session):
    tenant_id = uuid.uuid4()
    # Create test asset
    asset = AssetBusinessContext(
        tenant_id=tenant_id,
        asset_identifier="10.0.0.5",
        criticality_score=7.0,
        data_sensitivity="RESTRICTED"
    )
    db_session.add(asset)
    await db_session.commit()

    engine = BusinessImpactEngine(db_session)
    # Expected: (7.0 * 10) + 10 = 80.0
    score = await engine.calculate_impact("10.0.0.5", tenant_id)
    assert score == 80.0

async def test_business_impact_fallback(db_session):
    tenant_id = uuid.uuid4()
    engine = BusinessImpactEngine(db_session)
    # Unknown asset should return default 30.0
    score = await engine.calculate_impact("99.99.99.99", tenant_id)
    assert score == 30.0

async def test_priority_engine():
    # Engine logic does not strictly require DB access for calculate_priority
    engine = PriorityEngine(None)
    
    # Priority = (Threat * 0.6 + Impact * 0.4) * Confidence
    # Threat: 80, Impact: 90 -> Raw: 48 + 36 = 84
    # Confidence: 0.9 -> 84 * 0.9 = 75.6 -> HIGH
    
    result = await engine.calculate_priority(
        base_threat_severity=80.0,
        business_impact_score=90.0,
        confidence_multiplier=0.9
    )
    
    assert result["score"] == 75.6
    assert result["tier"] == "HIGH"

async def test_priority_engine_critical():
    engine = PriorityEngine(None)
    
    result = await engine.calculate_priority(
        base_threat_severity=100.0,
        business_impact_score=100.0,
        confidence_multiplier=0.95
    )
    
    # Raw: 60 + 40 = 100
    # Final: 95.0 -> CRITICAL
    assert result["score"] == 95.0
    assert result["tier"] == "CRITICAL"

import pytest
import uuid
from app.unified_timeline.timeline_manager import TimelineManager
from app.unified_timeline.correlation_engine import CorrelationEngine
from app.unified_timeline.relationship_engine import RelationshipEngine

pytestmark = pytest.mark.asyncio

async def test_session_creation(db_session):
    tenant_id = uuid.uuid4()
    mgr = TimelineManager(db_session)
    
    session = await mgr.create_unified_session(
        tenant_id=tenant_id,
        name="Operation Crimson Falcon"
    )
    
    assert session.id is not None
    assert session.name == "Operation Crimson Falcon"

async def test_event_correlation(db_session):
    mgr = TimelineManager(db_session)
    corr_eng = CorrelationEngine(db_session)
    
    session_id = uuid.uuid4()
    events = await mgr.import_mock_events(session_id)
    
    correlations = await corr_eng.correlate_events(session_id, events)
    
    assert len(correlations) > 0
    assert correlations[0].correlation_type == "SHARED_IP"
    assert correlations[0].correlation_value == "203.0.113.5"

async def test_causal_relationship(db_session):
    mgr = TimelineManager(db_session)
    rel_eng = RelationshipEngine(db_session)
    
    session_id = uuid.uuid4()
    events = await mgr.import_mock_events(session_id)
    
    relationships = await rel_eng.infer_causality(session_id, events)
    
    assert len(relationships) > 0
    assert relationships[0].correlation_type == "CAUSAL_SPAWN"

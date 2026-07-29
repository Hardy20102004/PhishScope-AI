import pytest
import uuid

from app.threat_hunting.query_engine import QueryEngine
from app.threat_hunting.hypothesis_engine import HypothesisEngine
from app.threat_hunting.hunt_manager import ThreatHuntManager

pytestmark = pytest.mark.asyncio

async def test_hypothesis_generation(db_session):
    session_id = uuid.uuid4()
    engine = HypothesisEngine(db_session)
    
    hypotheses = await engine.generate_hypotheses(session_id)
    
    assert len(hypotheses) == 2
    assert hypotheses[0].is_ai_generated is True
    assert hypotheses[0].confidence_score == 0.85
    assert "Credential Access" in hypotheses[0].mitre_tactics
    assert len(hypotheses[0].suggested_queries) > 0

async def test_natural_language_query_execution(db_session):
    session_id = uuid.uuid4()
    engine = QueryEngine(db_session)
    
    raw_query = "Find all powershell activity"
    query_record, results = await engine.execute_natural_language_search(session_id, raw_query)
    
    assert query_record.raw_query == raw_query
    assert query_record.query_type == "NATURAL_LANGUAGE"
    assert "powershell" in query_record.translated_structured_query["inferred_entities"]
    assert query_record.results_count == 1
    assert len(results) == 1

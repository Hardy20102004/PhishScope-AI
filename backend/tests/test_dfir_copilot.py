import pytest
import uuid
from app.schemas.dfir_copilot import DfirQuery
from app.dfir_copilot.conversation_engine import ConversationEngine

pytestmark = pytest.mark.asyncio

async def test_timeline_reasoning(db_session):
    engine = ConversationEngine(db_session)
    
    query = DfirQuery(
        conversation_id=uuid.uuid4(),
        investigation_id=uuid.uuid4(),
        content="Summarize the timeline.",
        context_type="TIMELINE"
    )
    
    response = await engine.process_query(query)
    
    assert response.message_id is not None
    assert len(response.chunks) > 0
    # Ensure strict classification is working
    classifications = [c.classification for c in response.chunks]
    assert "OBSERVATION" in classifications
    assert "ASSESSMENT" in classifications

async def test_artifact_explanation(db_session):
    engine = ConversationEngine(db_session)
    
    query = DfirQuery(
        conversation_id=uuid.uuid4(),
        investigation_id=uuid.uuid4(),
        content="Explain the Run registry key.",
        context_type="ARTIFACT"
    )
    
    response = await engine.process_query(query)
    
    assert len(response.chunks) > 0
    assert response.chunks[0].classification == "OBSERVATION"

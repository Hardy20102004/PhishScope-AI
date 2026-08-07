import pytest
import uuid

from app.soc_copilot.conversation_engine import ConversationEngine
from app.soc_copilot.reasoning_engine import ReasoningEngine

pytestmark = pytest.mark.asyncio

async def test_copilot_session_creation(db_session):
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    engine = ConversationEngine(db_session)
    session = await engine.create_session(
        title="Hunt APT29",
        context_tags=["APT29", "Lateral Movement"],
        tenant_id=tenant_id,
        user_id=user_id
    )
    
    assert session.id is not None
    assert session.title == "Hunt APT29"

async def test_copilot_reasoning_and_chat(db_session):
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    engine = ConversationEngine(db_session)
    session = await engine.create_session(
        title="Test Chat",
        context_tags=[],
        tenant_id=tenant_id,
        user_id=user_id
    )
    
    msg = await engine.send_message(session.id, "What is HR-05 doing?")
    
    assert msg.role == "ASSISTANT"
    assert "APT29" in msg.content
    assert len(msg.evidence_citations) > 0
    
    # Verify the reasoning log was created
    await db_session.refresh(session)
    assert len(session.reasoning_logs) == 1
    
    log = session.reasoning_logs[0]
    assert log.confidence_score > 0.9

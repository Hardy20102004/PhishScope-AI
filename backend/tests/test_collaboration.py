import pytest
import uuid

from app.collaboration.workspace_manager import WorkspaceManager
from app.collaboration.messaging_service import MessagingService
from app.collaboration.ai_collab_assistant import AICollabAssistant

pytestmark = pytest.mark.asyncio

async def test_workspace_messaging(db_session):
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    # Create workspace
    wm = WorkspaceManager(db_session)
    workspace = await wm.create_workspace(
        name="Test Incident Room",
        workspace_type="INCIDENT",
        tenant_id=tenant_id
    )
    
    assert workspace.id is not None
    assert workspace.name == "Test Incident Room"
    
    # Post messages
    ms = MessagingService(db_session)
    msg1 = await ms.post_message(
        workspace_id=workspace.id,
        sender_id=user_id,
        content="Hello team, starting investigation."
    )
    msg2 = await ms.post_message(
        workspace_id=workspace.id,
        sender_id=user_id,
        content="Found a malicious IP."
    )
    
    # Retrieve messages
    messages = await ms.get_messages(workspace.id)
    assert len(messages) == 2
    assert messages[0].id == msg1.id
    
def test_ai_thread_summarization():
    assistant = AICollabAssistant()
    
    # Mock some messages
    class MockMsg:
        def __init__(self, content):
            self.content = content
            
    msgs = [
        MockMsg("Hello team, starting investigation."),
        MockMsg("Found a malicious IP.")
    ]
    
    summary = assistant.summarize_thread(msgs)
    assert "AI Chat Summary" in summary

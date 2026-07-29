import pytest
import uuid

from app.soar.playbook_manager import PlaybookManager
from app.soar.execution_engine import ExecutionEngine
from app.soar.approval_engine import ApprovalEngine

pytestmark = pytest.mark.asyncio

async def test_playbook_execution_and_approval_flow(db_session):
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    # 1. Create Playbook
    pm = PlaybookManager(db_session)
    playbook = await pm.create_playbook(
        name="Test Playbook",
        description="A test workflow",
        tenant_id=tenant_id
    )
    
    assert playbook.id is not None
    
    # 2. Start Execution
    engine = ExecutionEngine(db_session)
    execution = await engine.start_execution(playbook.id)
    
    # Should pause at approval step
    assert execution.status == "PAUSED_FOR_APPROVAL"
    assert execution.current_step_id == "approval"
    
    # Assert Approval Record was created
    assert len(execution.approvals) == 1
    approval = execution.approvals[0]
    assert approval.status == "PENDING"
    
    # 3. Approve Action
    approver = ApprovalEngine(db_session)
    reviewed_approval = await approver.process_approval(
        approval_id=approval.id,
        user_id=user_id,
        approved=True,
        notes="Approved for testing"
    )
    
    assert reviewed_approval.status == "APPROVED"
    
    # 4. Assert Execution resumed and completed
    # Refresh execution object
    await db_session.refresh(execution)
    
    assert execution.status == "COMPLETED"
    assert execution.completed_at is not None
    assert execution.current_step_id is None
    
    # Check log
    log_steps = [log["step"] for log in execution.execution_log]
    assert "start" in log_steps
    assert "enrich" in log_steps
    assert "approval" in log_steps
    assert "isolate" in log_steps

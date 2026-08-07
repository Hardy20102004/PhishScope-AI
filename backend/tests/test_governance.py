import pytest
import uuid
from app.governance.workflow_engine import WorkflowEngine
from app.governance.approval_engine import ApprovalEngine
from app.governance.automation_orchestration_engine import AutomationOrchestrationEngine

pytestmark = pytest.mark.asyncio

async def test_governance_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Initialize Workflow
    we = WorkflowEngine(db_session)
    wf = await we.initialize_workflow(
        tenant_id, "Isolate Namespace", "REMEDIATION", {"namespace": "prod"}
    )
    
    assert wf.status == "PENDING_APPROVAL"
    
    # 2. Test Rejection from L1
    ae = ApprovalEngine(db_session)
    await ae.submit_approval(tenant_id, wf.id, "analyst_bob", "L1_SOC", "REJECTED")
    
    # Refresh wf
    await db_session.refresh(wf)
    assert wf.status == "REJECTED"
    
    # 3. Test Successful CISO Approval
    wf2 = await we.initialize_workflow(
        tenant_id, "Isolate Namespace 2", "REMEDIATION", {"namespace": "prod2"}
    )
    
    await ae.submit_approval(tenant_id, wf2.id, "ciso_alice", "CISO", "APPROVED")
    
    await db_session.refresh(wf2)
    assert wf2.status == "APPROVED_FOR_EXECUTION"
    
    # 4. Test Automation Execution
    aoe = AutomationOrchestrationEngine(db_session)
    log = await aoe.execute_task(wf2, "Apply NetworkPolicy", {"target": "prod2"})
    
    assert log.status == "SUCCESS"
    assert wf2.status == "COMPLETED"
    
    # 5. Test Automation Blocker
    wf3 = await we.initialize_workflow(tenant_id, "Blocker Test", "REMEDIATION", {})
    with pytest.raises(ValueError):
        await aoe.execute_task(wf3, "Delete Role", {})

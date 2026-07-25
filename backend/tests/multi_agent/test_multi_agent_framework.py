import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.multi_agent.communication import CommunicationBus
from app.multi_agent.human import HumanInTheLoopEngine
from app.models.multi_agent import ApprovalStatus, MessageType

@pytest.mark.asyncio
async def test_communication_bus_broadcast():
    bus = CommunicationBus()
    
    # Track received messages
    received = []
    def callback(msg):
        received.append(msg)
        
    bus.subscribe("threat-intel-agent", callback)
    
    msg_id = await bus.publish(
        sender_id="investigator-agent",
        message_type=MessageType.BROADCAST,
        content={"data": "test broadcast"}
    )
    
    assert len(received) == 1
    assert received[0]["id"] == msg_id
    assert received[0]["content"]["data"] == "test broadcast"

@pytest.mark.asyncio
async def test_human_in_the_loop_approval():
    bus = CommunicationBus()
    hitl = HumanInTheLoopEngine(bus)
    
    # Request approval
    req = hitl.request_approval(
        task_id="f47ac10b-58cc-4372-a567-0e02b2c3d479",
        agent_id="recommendation-agent",
        description="Block 10.0.0.5 on firewall",
        severity="HIGH"
    )
    
    assert req.status == ApprovalStatus.PENDING
    assert len(hitl.get_pending_approvals()) == 1
    
    # Submit decision
    resolved = hitl.submit_decision(
        request_id=str(req.id),
        reviewer_id="550e8400-e29b-41d4-a716-446655440000",
        status=ApprovalStatus.APPROVED,
        feedback="Looks good to block."
    )
    
    assert resolved.status == ApprovalStatus.APPROVED
    assert len(hitl.get_pending_approvals()) == 0

@pytest.mark.asyncio
async def test_human_in_the_loop_override():
    bus = CommunicationBus()
    hitl = HumanInTheLoopEngine(bus)
    
    req = hitl.request_approval(
        task_id="3d813cbb-47fb-42ba-91df-831e1593ac29",
        agent_id="malware-analysis-agent",
        description="Quarantine entire subnet",
        severity="CRITICAL"
    )
    
    resolved = hitl.submit_decision(
        request_id=str(req.id),
        reviewer_id="550e8400-e29b-41d4-a716-446655440000",
        status=ApprovalStatus.OVERRIDDEN,
        feedback="Too broad, blocking specific IP instead."
    )
    
    assert resolved.status == ApprovalStatus.OVERRIDDEN

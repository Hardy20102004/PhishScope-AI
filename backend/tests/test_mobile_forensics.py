import pytest
import uuid
from datetime import datetime, timezone

from app.models.mobile_forensics import ForensicMobileDevice
from app.mobile_forensics.device_manager import DeviceManager
from app.mobile_forensics.communication_engine import CommunicationEngine
from app.mobile_forensics.location_engine import LocationEngine
from app.mobile_forensics.timeline_builder import TimelineBuilder

pytestmark = pytest.mark.asyncio

async def test_device_registration(db_session):
    tenant_id = uuid.uuid4()
    mgr = DeviceManager(db_session)
    
    device = await mgr.register_device(
        tenant_id=tenant_id,
        name="Suspect_iPhone",
        os_type="iOS",
        os_version="17.2",
        acq_type="iTunes Backup"
    )
    
    assert device.id is not None
    assert device.os_type == "iOS"

async def test_communication_extraction(db_session):
    tenant_id = uuid.uuid4()
    mgr = DeviceManager(db_session)
    device = await mgr.register_device(
        tenant_id=tenant_id,
        name="Test",
        os_type="Android",
        os_version="14",
        acq_type="ADB Logical"
    )
    
    engine = CommunicationEngine(db_session)
    messages = await engine.extract_messages(device.id)
    
    assert len(messages) > 0
    assert any(m.is_deleted == True for m in messages)

async def test_unified_timeline_builder():
    builder = TimelineBuilder()
    
    class MockComm:
        timestamp = datetime(2026, 7, 27, 14, 0, tzinfo=timezone.utc)
        app_name = "SMS"
        is_outgoing = True
        receiver = "123"
        body = "Hello"
        
    class MockLoc:
        timestamp = datetime(2026, 7, 27, 14, 30, tzinfo=timezone.utc)
        source = "GPS"
        latitude = 0.0
        longitude = 0.0
        accuracy_meters = 10
        
    timeline = builder.generate_timeline([MockComm()], [MockLoc()])
    
    assert len(timeline) == 2
    # Ensure chronological order
    assert timeline[0]["type"] == "MESSAGE"
    assert timeline[1]["type"] == "LOCATION"

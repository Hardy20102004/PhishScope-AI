import pytest
import uuid
from datetime import datetime, timezone

from app.models.memory_forensics import MemoryImage
from app.memory_forensics.image_manager import ImageManager
from app.memory_forensics.process_engine import ProcessEngine
from app.memory_forensics.network_engine import NetworkEngine

pytestmark = pytest.mark.asyncio

async def test_image_registration_and_os_profile(db_session):
    tenant_id = uuid.uuid4()
    mgr = ImageManager(db_session)
    
    image = await mgr.register_image(
        tenant_id=tenant_id,
        filename="RAM-DUMP.vmem",
        os_profile="Win10x64_19041",
        size=16000000000
    )
    
    assert image.id is not None
    assert image.os_profile == "Win10x64_19041"

async def test_process_extraction_and_dkom(db_session):
    tenant_id = uuid.uuid4()
    mgr = ImageManager(db_session)
    image = await mgr.register_image(
        tenant_id=tenant_id,
        filename="RAM-DUMP.vmem",
        os_profile="Win10",
        size=16000000000
    )
    
    engine = ProcessEngine(db_session)
    processes = await engine.extract_processes(image.id)
    
    assert len(processes) > 0
    
    # Verify DKOM detection logic works (svchost is unlinked/hidden)
    hidden_proc = next(p for p in processes if p.name == "svchost.exe")
    assert hidden_proc.is_hidden == True
    assert hidden_proc.is_injected == True

async def test_network_socket_extraction(db_session):
    tenant_id = uuid.uuid4()
    mgr = ImageManager(db_session)
    image = await mgr.register_image(
        tenant_id=tenant_id,
        filename="RAM-DUMP.vmem",
        os_profile="Win10",
        size=16000000000
    )
    
    engine = NetworkEngine(db_session)
    connections = await engine.extract_connections(image.id)
    
    assert len(connections) > 0
    assert any(c.state == "ESTABLISHED" for c in connections)
    assert any(c.state == "LISTENING" for c in connections)

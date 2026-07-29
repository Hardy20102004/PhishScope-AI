import pytest
import uuid
from datetime import datetime, timezone

from app.models.browser_forensics import BrowserProfile
from app.browser_forensics.profile_manager import ProfileManager
from app.browser_forensics.history_engine import HistoryEngine
from app.browser_forensics.extension_engine import ExtensionEngine
from app.browser_forensics.timeline_builder import TimelineBuilder

pytestmark = pytest.mark.asyncio

async def test_profile_registration(db_session):
    tenant_id = uuid.uuid4()
    mgr = ProfileManager(db_session)
    
    profile = await mgr.register_profile(
        tenant_id=tenant_id,
        browser_type="Google Chrome",
        profile_name="Default",
        host_os="Windows 10"
    )
    
    assert profile.id is not None
    assert profile.browser_type == "Google Chrome"

async def test_history_extraction(db_session):
    tenant_id = uuid.uuid4()
    mgr = ProfileManager(db_session)
    profile = await mgr.register_profile(
        tenant_id=tenant_id,
        browser_type="Chrome",
        profile_name="Test",
        host_os="Windows"
    )
    
    engine = HistoryEngine(db_session)
    history = await engine.extract_history(profile.id)
    
    assert len(history) > 0
    assert any(h.is_threat_hit == True for h in history)

def test_timeline_generation():
    builder = TimelineBuilder()
    
    class MockHistory:
        timestamp = datetime(2026, 7, 27, 14, 0, tzinfo=timezone.utc)
        url = "http://evil.com"
        title = "Evil"
        is_threat_hit = True
        
    class MockExt:
        install_time = datetime(2026, 7, 27, 14, 30, tzinfo=timezone.utc)
        name = "Bad Ext"
        version = "1.0"
        is_suspicious = True
        
    timeline = builder.generate_timeline([MockHistory()], [MockExt()])
    
    assert len(timeline) == 2
    assert timeline[0]["type"] == "PAGE_VISIT"
    assert timeline[1]["type"] == "EXTENSION_INSTALL"

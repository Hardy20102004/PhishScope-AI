import pytest
import uuid
from datetime import datetime, timezone

from app.models.email_forensics import Mailbox
from app.email_forensics.mailbox_manager import MailboxManager
from app.email_forensics.message_parser import MessageParser
from app.email_forensics.auth_engine import AuthEngine
from app.email_forensics.routing_engine import RoutingEngine

pytestmark = pytest.mark.asyncio

async def test_mailbox_registration(db_session):
    tenant_id = uuid.uuid4()
    mgr = MailboxManager(db_session)
    
    mailbox = await mgr.register_mailbox(
        tenant_id=tenant_id,
        name="Phishing_01.eml",
        source_type="EML",
        owner_email="victim@company.com"
    )
    
    assert mailbox.id is not None
    assert mailbox.source_type == "EML"

async def test_auth_engine_parsing(db_session):
    engine = AuthEngine(db_session)
    msg_id = uuid.uuid4()
    
    # Test Spoofed Email
    header = await engine.analyze_auth(message_id=msg_id, is_phish=True)
    
    assert header.header_name == "Authentication-Results"
    assert header.parsed_data["spf"] == "fail"
    assert header.parsed_data["dmarc"] == "fail"

async def test_routing_engine_hop_parsing(db_session):
    engine = RoutingEngine(db_session)
    msg_id = uuid.uuid4()
    
    headers = await engine.analyze_routing(message_id=msg_id, is_phish=True)
    
    assert len(headers) == 3
    assert headers[0].hop_index == 1
    assert "unknown (103.22.1.5)" in headers[0].header_value

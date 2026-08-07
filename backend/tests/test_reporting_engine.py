import pytest
import uuid
from app.reporting_engine.custody_engine import CustodyEngine
from app.reporting_engine.report_manager import ReportManager
from app.reporting_engine.generation_engine import GenerationEngine

pytestmark = pytest.mark.asyncio

async def test_custody_engine_ingest(db_session):
    tenant_id = uuid.uuid4()
    engine = CustodyEngine(db_session)
    
    item = await engine.ingest_evidence(
        tenant_id=tenant_id,
        name="server01_disk.e01",
        source_type="DISK_IMAGE",
        original_hash="8b5a6c1e9f...",
        actor_id="analyst1"
    )
    
    assert item.id is not None
    assert len(item.chain_of_custody) == 1
    assert item.chain_of_custody[0].action_type == "INGEST"
    assert item.chain_of_custody[0].record_hash is not None

async def test_report_scaffolding(db_session):
    tenant_id = uuid.uuid4()
    mgr = ReportManager(db_session)
    
    report = await mgr.initialize_report(
        tenant_id=tenant_id,
        title="Test Incident Report",
        report_type="TECHNICAL",
        author_id="admin@company.com"
    )
    
    assert report.id is not None
    assert len(report.sections) == 3
    assert report.sections[0].section_type == "EXECUTIVE_SUMMARY"

async def test_report_generation(db_session):
    tenant_id = uuid.uuid4()
    mgr = ReportManager(db_session)
    gen = GenerationEngine(db_session)
    
    report = await mgr.initialize_report(
        tenant_id=tenant_id,
        title="Final Report",
        report_type="COURT_READY",
        author_id="admin@company.com"
    )
    
    final_report = await gen.finalize_report(report.id)
    
    assert final_report.is_finalized is True
    assert final_report.digital_signature is not None

import pytest
import uuid
from datetime import datetime, timezone

from app.models.disk_forensics import DiskImage
from app.disk_forensics.image_manager import ImageManager
from app.disk_forensics.fs_analysis_engine import FileSystemAnalysisEngine
from app.disk_forensics.timeline_builder import TimelineBuilder

pytestmark = pytest.mark.asyncio

async def test_image_registration_and_hashing(db_session):
    tenant_id = uuid.uuid4()
    mgr = ImageManager(db_session)
    
    image = await mgr.register_image(
        tenant_id=tenant_id,
        filename="EVIDENCE-01.E01",
        format="E01",
        size=1024000,
        md5="d41d8cd98f00b204e9800998ecf8427e",
        sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    
    assert image.id is not None
    assert image.hash_verified == True

async def test_fs_parsing(db_session):
    tenant_id = uuid.uuid4()
    mgr = ImageManager(db_session)
    image = await mgr.register_image(
        tenant_id=tenant_id,
        filename="EVIDENCE-02.DD",
        format="RAW",
        size=1024000,
        md5="mock",
        sha256="mock"
    )
    
    fs_engine = FileSystemAnalysisEngine(db_session)
    partitions = await fs_engine.parse_image(image.id)
    
    assert len(partitions) > 0
    assert partitions[0].partition_type == "NTFS"
    assert len(partitions[0].artifacts) > 0

async def test_timeline_builder():
    builder = TimelineBuilder()
    timeline = builder.generate_timeline()
    
    assert len(timeline) == 3
    assert any(e["event_type"] == "CREATED" for e in timeline)
    assert any(e["event_type"] == "DELETED" for e in timeline)

import pytest
import uuid
from app.dspm.data_discovery_engine import DataDiscoveryEngine
from app.dspm.data_classification_engine import DataClassificationEngine
from app.dspm.exposure_analysis_engine import ExposureAnalysisEngine
from app.dspm.encryption_assessment_engine import EncryptionAssessmentEngine

pytestmark = pytest.mark.asyncio

async def test_dspm_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Discovery
    dde = DataDiscoveryEngine(db_session)
    asset = await dde.register_asset(
        tenant_id, "prod-customer-backups-2026", "AWS", "S3", "us-east-1", is_public=True, is_encrypted=False
    )
    
    assert asset.asset_name == "prod-customer-backups-2026"
    assert asset.is_public is True
    
    # 2. Test Classification
    dce = DataClassificationEngine(db_session)
    classification = await dce.classify_asset(asset, "PII", 0.95)
    
    assert classification.label == "PII"
    assert classification.requires_review is False
    
    # 3. Test Exposure Analysis
    eae = ExposureAnalysisEngine(db_session)
    findings = await eae.analyze_exposure(asset)
    
    # Should flag CRITICAL because it is public AND contains PII
    assert len(findings) == 1
    assert findings[0].finding_type == "PUBLIC_ACCESS"
    assert findings[0].severity == "CRITICAL"
    
    # 4. Test Encryption Assessment
    enc_engine = EncryptionAssessmentEngine(db_session)
    enc_finding = await enc_engine.assess_encryption(asset)
    
    # Should flag HIGH because it is unencrypted
    assert enc_finding is not None
    assert enc_finding.finding_type == "UNENCRYPTED_AT_REST"
    assert enc_finding.severity == "HIGH"

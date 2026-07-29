import pytest
import uuid
from app.cspm.asset_discovery_engine import CSPMCloudAssetDiscoveryEngine
from app.cspm.compliance_engine import ComplianceEngine
from app.cspm.risk_assessment_engine import RiskAssessmentEngine

pytestmark = pytest.mark.asyncio

async def test_cspm_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Asset Discovery
    ade = CSPMCloudAssetDiscoveryEngine(db_session)
    config = {"publicly_accessible": True, "encrypted": False}
    asset = await ade.register_asset(tenant_id, "AWS", "Storage", "public-assets-bucket", "us-west-2", config)
    
    assert asset.asset_name == "public-assets-bucket"
    assert asset.provider == "AWS"
    
    # 2. Test Risk Assessment
    rae = RiskAssessmentEngine(db_session)
    misc = await rae.evaluate_asset_risk(asset)
    
    assert misc.severity == "CRITICAL"
    assert "Unencrypted Public Resource" in misc.title
    assert misc.asset_id == asset.id
    
    # 3. Test Compliance Mapping
    ce = ComplianceEngine(db_session)
    finding = await ce.log_compliance_finding(tenant_id, "CIS_AWS_v1.4", "2.1.1", passed=42, failed=6)
    
    assert finding.framework == "CIS_AWS_v1.4"
    assert finding.failed == 6

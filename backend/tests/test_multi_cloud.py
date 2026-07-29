import pytest
import uuid
from app.multi_cloud.unified_asset_engine import UnifiedAssetEngine
from app.multi_cloud.cross_cloud_correlation_engine import CrossCloudCorrelationEngine
from app.multi_cloud.unified_risk_engine import UnifiedRiskEngine
from app.multi_cloud.compliance_analytics_engine import ComplianceAnalyticsEngine

pytestmark = pytest.mark.asyncio

async def test_multi_cloud_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Unified Asset Registry
    uae = UnifiedAssetEngine(db_session)
    asset_aws = await uae.register_asset(
        tenant_id, "prod-web-01", "AWS", "COMPUTE", "PROD", "i-0abcd123"
    )
    asset_azure = await uae.register_asset(
        tenant_id, "analytics-db", "AZURE", "STORAGE", "PROD", "sub/db"
    )
    
    assert asset_aws.provider == "AWS"
    assert asset_azure.provider == "AZURE"
    
    # 2. Test Cross-Cloud Correlation
    cce = CrossCloudCorrelationEngine(db_session)
    link = await cce.link_assets(tenant_id, asset_aws, asset_azure, "COMMUNICATES_WITH")
    
    assert link.source_asset_id == asset_aws.id
    assert link.target_asset_id == asset_azure.id
    
    # 3. Test Unified Risk Engine (Critical Path Strategy)
    ure = UnifiedRiskEngine(db_session)
    risk_score = await ure.calculate_enterprise_risk(tenant_id, critical_findings_count=10)
    
    # 100 base + (10 * 50 * 1.5) = 850
    assert risk_score.global_score == 850.0
    
    # 4. Test Compliance Engine
    cae = ComplianceAnalyticsEngine(db_session)
    trend = await cae.record_trend(tenant_id, "NIST_CSF", 85.5, 12)
    
    assert trend.framework == "NIST_CSF"
    assert trend.compliance_percentage == 85.5

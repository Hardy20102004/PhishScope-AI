import pytest
import uuid
from datetime import datetime, timezone, timedelta
from app.ciem.identity_discovery_engine import IdentityDiscoveryEngine
from app.ciem.least_privilege_engine import LeastPrivilegeEngine
from app.ciem.identity_risk_engine import IdentityRiskEngine
from app.ciem.entitlement_analysis_engine import EntitlementAnalysisEngine

pytestmark = pytest.mark.asyncio

async def test_ciem_workflows(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Test Discovery
    ide = IdentityDiscoveryEngine(db_session)
    # Simulate a dormant user without MFA
    dormant_date = datetime.now(timezone.utc) - timedelta(days=100)
    identity = await ide.register_identity(tenant_id, "bob@corp.com", "USER", "AWS", "12345", mfa=False, last_login=dormant_date)
    
    assert identity.identity_name == "bob@corp.com"
    
    # 2. Add Entitlements
    eae = EntitlementAnalysisEngine(db_session)
    await eae.record_entitlement(tenant_id, identity.id, "iam:role", "*", is_admin=True)
    
    # 3. Test Least Privilege Hygiene
    lpe = LeastPrivilegeEngine(db_session)
    risk_factors = await lpe.evaluate_identity_hygiene(identity)
    
    assert "No MFA Configured" in risk_factors
    assert "Dormant Identity (>90 Days)" in risk_factors
    assert "Holds Administrative Privilege" in risk_factors
    
    # 4. Test Risk Aggregation
    ire = IdentityRiskEngine(db_session)
    risk_score = await ire.update_risk_score(tenant_id, identity)
    
    # 30 (MFA) + 30 (Dormant) + 40 (Admin) = 100
    assert risk_score.risk_score == 100.0

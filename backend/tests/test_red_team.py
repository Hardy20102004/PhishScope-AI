import pytest
import uuid
from app.red_team.campaign_manager import CampaignManager
from app.red_team.authorization_manager import AuthorizationManager
from app.models.red_team import RedTeamCampaign, AuthorizationRecord
from sqlalchemy import select

pytestmark = pytest.mark.asyncio

async def test_campaign_approval_workflow(db_session):
    tenant_id = uuid.uuid4()
    
    # 1. Create Campaign
    mgr = CampaignManager(db_session)
    campaign = await mgr.create_campaign(
        tenant_id=tenant_id,
        name="Ransomware Sim",
        description="Test defenses against encryption.",
        scope={"in_scope": ["10.0.0.0/24"]}
    )
    
    assert campaign.status == "DRAFT"
    
    # 2. Request Auth
    campaign = await mgr.request_authorization(campaign.id)
    assert campaign.status == "PENDING_APPROVAL"
    
    # 3. Cannot start without approvals
    with pytest.raises(PermissionError):
        await mgr.commence_campaign(campaign.id)
        
    # 4. Sign Approvals
    auth_mgr = AuthorizationManager(db_session)
    res = await db_session.execute(select(AuthorizationRecord).where(AuthorizationRecord.campaign_id == campaign.id))
    auths = res.scalars().all()
    
    for auth in auths:
        await auth_mgr.sign_authorization(auth.id, f"{auth.stakeholder_role}@company.com")
        
    # 5. Check if auto-progressed to AUTHORIZED
    db_session.expire_all()
    res = await db_session.execute(select(RedTeamCampaign).where(RedTeamCampaign.id == campaign.id))
    updated_camp = res.scalar_one()
    
    assert updated_camp.status == "AUTHORIZED"
    
    # 6. Can now commence
    final_camp = await mgr.commence_campaign(updated_camp.id)
    assert final_camp.status == "IN_PROGRESS"

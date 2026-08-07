from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.zta import ZTAAccessDecision, AccessDecision, PolicyEffect
from app.zta.policy_engine import ZeroTrustPolicyEngine
from app.zta.verification_engine import ContinuousVerificationEngine

class AdaptiveAccessEngine:
    """
    Evaluates context against policies to render adaptive access decisions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.policy_engine = ZeroTrustPolicyEngine(db)
        self.verification_engine = ContinuousVerificationEngine(db)

    async def evaluate_access(
        self, tenant_id: uuid.UUID, context_snapshot_id: uuid.UUID, snapshot_data: Dict[str, Any], resource_requested: str
    ) -> ZTAAccessDecision:
        
        # 1. Run verifications
        verifications = await self.verification_engine.run_full_verification(tenant_id, context_snapshot_id, snapshot_data)
        failed_verifications = [v for v in verifications if not v.is_valid]
        
        if failed_verifications:
            decision = AccessDecision.DENY
            rationale = "Denied due to failed continuous verification checks."
            matched = []
        else:
            # 2. Evaluate policies
            policy_result = await self.policy_engine.evaluate_context_against_policies(tenant_id, snapshot_data)
            
            effect = policy_result["effect"]
            if effect == PolicyEffect.DENY:
                decision = AccessDecision.DENY
            elif effect == PolicyEffect.CHALLENGE:
                decision = AccessDecision.STEP_UP_AUTH
                if "REQUIRE_MFA" in policy_result["actions"]:
                    decision = AccessDecision.REQUIRE_MFA
            else:
                decision = AccessDecision.ALLOW
                
            rationale = policy_result["rationale"]
            matched = policy_result["matched_policies"]

        access_decision = ZTAAccessDecision(
            tenant_id=tenant_id,
            context_snapshot_id=context_snapshot_id,
            decision=decision,
            matched_policy_ids=matched,
            rationale=rationale,
            resource_requested=resource_requested
        )
        self.db.add(access_decision)
        await self.db.commit()
        await self.db.refresh(access_decision)
        return access_decision

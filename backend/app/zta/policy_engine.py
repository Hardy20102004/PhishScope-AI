from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.zta import ZTAPolicy, PolicyEffect

class ZeroTrustPolicyEngine:
    """
    Zero Trust Policy Engine.
    Manages and evaluates access policies based on context.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_policies(self, tenant_id: uuid.UUID) -> List[ZTAPolicy]:
        result = await self.db.execute(
            select(ZTAPolicy).where(ZTAPolicy.tenant_id == tenant_id).order_by(ZTAPolicy.priority.asc())
        )
        return result.scalars().all()

    async def create_policy(self, tenant_id: uuid.UUID, data: Dict[str, Any]) -> ZTAPolicy:
        policy = ZTAPolicy(
            tenant_id=tenant_id,
            name=data["name"],
            description=data.get("description"),
            is_active=data.get("is_active", True),
            priority=data.get("priority", 100),
            conditions=data.get("conditions", {}),
            effect=PolicyEffect(data["effect"]),
            actions=data.get("actions", [])
        )
        self.db.add(policy)
        await self.db.commit()
        await self.db.refresh(policy)
        return policy

    async def evaluate_context_against_policies(
        self, tenant_id: uuid.UUID, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate context against all active policies in priority order.
        In a real scenario, this would use a robust rules engine.
        For now, we simulate evaluation.
        """
        policies = await self.get_policies(tenant_id)
        active_policies = [p for p in policies if p.is_active]
        
        matched_policies = []
        final_effect = PolicyEffect.ALLOW
        actions = []
        
        # Simulated logic: if any policy condition matches, apply effect.
        # Here we just take the first policy for simplicity if it exists.
        for policy in active_policies:
            # Simulating condition match
            match = True
            if policy.conditions.get("require_mfa") and not context.get("auth_context", {}).get("mfa_active"):
                match = False
            
            if match:
                matched_policies.append(str(policy.id))
                final_effect = policy.effect
                actions.extend(policy.actions)
                break
                
        return {
            "matched_policies": matched_policies,
            "effect": final_effect,
            "actions": actions,
            "rationale": f"Evaluated against {len(active_policies)} active policies."
        }

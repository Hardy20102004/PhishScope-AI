import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ciem import CIEMCloudIdentity, CloudEntitlement
from sqlalchemy import select

class LeastPrivilegeEngine:
    """
    Identifies unused, dormant, or excessively broad permissions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def evaluate_identity_hygiene(self, identity: CIEMCloudIdentity) -> list[str]:
        """Returns a list of risk factors for the identity."""
        risk_factors = []
        
        # Check MFA
        if identity.identity_type == "USER" and not identity.mfa_enabled:
            risk_factors.append("No MFA Configured")
            
        # Check Dormancy (90 days)
        if identity.last_login:
            last_login = identity.last_login
            if last_login.tzinfo is None:
                last_login = last_login.replace(tzinfo=timezone.utc)
            days_since_login = (datetime.now(timezone.utc) - last_login).days
            if days_since_login > 90:
                risk_factors.append("Dormant Identity (>90 Days)")
                
        # Check for admin entitlements
        res = await self.db.execute(select(CloudEntitlement).where(
            CloudEntitlement.identity_id == identity.id,
            CloudEntitlement.is_admin_privilege == True
        ))
        if res.scalars().first():
            risk_factors.append("Holds Administrative Privilege")
            
        return risk_factors

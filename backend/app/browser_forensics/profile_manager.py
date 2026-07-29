import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.browser_forensics import BrowserProfile

class ProfileManager:
    """
    Handles ingestion of browser profiles (Default, Profile 1, etc).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_profile(self, tenant_id: uuid.UUID, browser_type: str, profile_name: str, host_os: str, inv_id: uuid.UUID = None) -> BrowserProfile:
        profile = BrowserProfile(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            browser_type=browser_type,
            profile_name=profile_name,
            host_os=host_os
        )
        
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

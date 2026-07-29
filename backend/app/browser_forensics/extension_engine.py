import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.browser_forensics import BrowserExtension

class ExtensionEngine:
    """
    Simulates parsing browser extension manifests (manifest.json) to detect malicious side-loading.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def extract_extensions(self, profile_id: uuid.UUID) -> list[BrowserExtension]:
        now = datetime.now(timezone.utc)
        
        # Mocking extracted extensions
        extensions = [
            BrowserExtension(
                profile_id=profile_id,
                extension_id="cjpalhdlnbpafiamejdnhcphjbkeiagm",
                name="uBlock Origin",
                version="1.54.0",
                description="Finally, an efficient blocker. Easy on CPU and memory.",
                permissions="<all_urls>, storage, tabs, webRequest",
                is_suspicious=False,
                install_time=now - timedelta(days=100)
            ),
            BrowserExtension(
                profile_id=profile_id,
                extension_id="aohfdmjgnbmmghihhfgjkjehmfdjebhi",
                name="Free PDF Converter Tool",
                version="2.1",
                description="Convert PDF to Word",
                permissions="<all_urls>, tabs, cookies, webRequest, webRequestBlocking", # Highly suspicious for a PDF tool
                is_suspicious=True, # Marked suspicious due to excessive permissions vs stated functionality
                install_time=now - timedelta(days=1)
            )
        ]
        
        for ext in extensions:
            self.db.add(ext)
            
        await self.db.commit()
        return extensions

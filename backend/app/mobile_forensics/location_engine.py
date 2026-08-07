import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.mobile_forensics import ForensicMobileLocation

class LocationEngine:
    """
    Simulates extracting GPS coordinates from cache.db or photo EXIF data.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def extract_locations(self, device_id: uuid.UUID) -> list[ForensicMobileLocation]:
        now = datetime.now(timezone.utc)
        
        # Mocking GPS data
        locations = [
            ForensicMobileLocation(
                device_id=device_id,
                source="CoreLocation Cache",
                latitude=37.7749,
                longitude=-122.4194, # San Francisco
                accuracy_meters=15.0,
                timestamp=now - timedelta(days=1, hours=2)
            ),
            ForensicMobileLocation(
                device_id=device_id,
                source="Photo EXIF",
                latitude=37.7750,
                longitude=-122.4180,
                accuracy_meters=5.0,
                timestamp=now - timedelta(days=1, hours=1)
            )
        ]
        
        for loc in locations:
            self.db.add(loc)
            
        await self.db.commit()
        return locations

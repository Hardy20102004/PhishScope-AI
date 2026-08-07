from typing import List
from sqlalchemy.orm import Session
from app.models.cyber_os import PlatformRegistryEntry
from app.schemas.cyber_os import PlatformRegistryEntryCreate

class RegistryService:
    def __init__(self, db: Session):
        self.db = db

    def register_module(self, entry_in: PlatformRegistryEntryCreate) -> PlatformRegistryEntry:
        db_entry = PlatformRegistryEntry(
            module_name=entry_in.module_name,
            version=entry_in.version,
            api_endpoint_prefix=entry_in.api_endpoint_prefix,
            capabilities=entry_in.capabilities,
            status=entry_in.status
        )
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        return db_entry

    def get_registered_modules(self, skip: int = 0, limit: int = 100) -> List[PlatformRegistryEntry]:
        return self.db.query(PlatformRegistryEntry).offset(skip).limit(limit).all()

import uuid

from sqlalchemy.orm import Session

from app.models.reporting import ExportFormat, ExportRecord
from app.services.custody_service import CustodyService


class ExportService:
    def __init__(self, db: Session):
        self.db = db
        self.custody = CustodyService(db)
        
    def generate_case_export(self, case_id: uuid.UUID, fmt: ExportFormat, user_id: uuid.UUID) -> ExportRecord:
        # Stub: Generate the actual ZIP/JSON file, hash it, and store it.
        # We will just generate a manifest to represent the "export content" and hash that.
        manifest = self.custody.generate_manifest(case_id, user_id)
        
        record = ExportRecord(
            target_id=case_id,
            target_type="CASE",
            format=fmt,
            file_hash=manifest.hash_value,
            created_by=user_id
        )
        
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        
        return record

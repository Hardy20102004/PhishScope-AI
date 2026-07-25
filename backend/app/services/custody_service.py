import hashlib
import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case_management import Case
from app.models.reporting import EvidenceManifest


class CustodyService:
    def __init__(self, db: Session):
        self.db = db
        
    def generate_manifest(self, case_id: uuid.UUID, user_id: uuid.UUID) -> EvidenceManifest:
        # Fetch case data to hash
        stmt = select(Case).where(Case.id == case_id)
        case = self.db.execute(stmt).scalar_one_or_none()
        if not case:
            raise ValueError("Case not found")
            
        # Build manifest structure
        manifest_data = {
            "case_id": str(case.id),
            "title": case.title,
            "created_at": case.created_at.isoformat(),
            # In a real scenario, this would iterate over evidence, timeline, etc.
            "evidence_count": len(case.investigations),
            "timeline_count": len(case.timeline_events)
        }
        
        manifest_json_str = json.dumps(manifest_data, sort_keys=True)
        hash_val = hashlib.sha256(manifest_json_str.encode('utf-8')).hexdigest()
        
        manifest = EvidenceManifest(
            case_id=case_id,
            manifest_json=manifest_data,
            hash_value=hash_val,
            created_by=user_id
        )
        self.db.add(manifest)
        self.db.commit()
        self.db.refresh(manifest)
        
        return manifest
        
    def verify_manifest(self, manifest_json: dict, provided_hash: str) -> bool:
        manifest_json_str = json.dumps(manifest_json, sort_keys=True)
        computed_hash = hashlib.sha256(manifest_json_str.encode('utf-8')).hexdigest()
        return computed_hash == provided_hash

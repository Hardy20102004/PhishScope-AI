import uuid
import hashlib
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.reporting_engine import ForensicReport

class GenerationEngine:
    """
    Finalizes and digitally signs a report for court or executive distribution.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def finalize_report(self, report_id: uuid.UUID) -> ForensicReport:
        result = await self.db.execute(select(ForensicReport).where(ForensicReport.id == report_id))
        report = result.scalar_one_or_none()
        if not report:
            raise ValueError("Report not found")
            
        # Prevent re-finalization
        if report.is_finalized:
            return report
            
        # In a real system, we would concatenate the content of all sections,
        # the author ID, and the timestamp, and sign it with the organization's private key.
        # Here we simulate the signature using a simple SHA-256 hash.
        
        signature_material = f"{report.id}:{report.title}:{datetime.now(timezone.utc).isoformat()}"
        digital_signature = hashlib.sha256(signature_material.encode('utf-8')).hexdigest()
        
        report.is_finalized = True
        report.digital_signature = digital_signature
        
        await self.db.commit()
        return report

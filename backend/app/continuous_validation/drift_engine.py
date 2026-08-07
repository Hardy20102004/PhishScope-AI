import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.continuous_validation import SecurityDriftRecord, SecurityPostureSnapshot

class SecurityDriftEngine:
    """
    Monitors for regressions (drift) in security posture over time.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_for_drift(self, tenant_id: uuid.UUID) -> list[SecurityDriftRecord]:
        # Pull the two most recent snapshots to compare
        res = await self.db.execute(
            select(SecurityPostureSnapshot)
            .where(SecurityPostureSnapshot.tenant_id == tenant_id)
            .order_by(desc(SecurityPostureSnapshot.timestamp))
            .limit(2)
        )
        snapshots = res.scalars().all()
        
        drifts = []
        if len(snapshots) == 2:
            current = snapshots[0]
            previous = snapshots[1]
            
            # Check for significant drops (> 10%)
            if (previous.overall_posture_score - current.overall_posture_score) > 10.0:
                record = SecurityDriftRecord(
                    tenant_id=tenant_id,
                    drift_type="POSTURE_DEGRADATION",
                    severity="HIGH",
                    description=f"Overall Security Posture Score dropped by {previous.overall_posture_score - current.overall_posture_score:.1f} points since the last snapshot.",
                    baseline_value=previous.overall_posture_score,
                    current_value=current.overall_posture_score
                )
                self.db.add(record)
                drifts.append(record)
                
            if (previous.control_effectiveness - current.control_effectiveness) > 15.0:
                record = SecurityDriftRecord(
                    tenant_id=tenant_id,
                    drift_type="CONTROL_FAILURE",
                    severity="CRITICAL",
                    description="Automated BAS validation detected a critical drop in Control Effectiveness.",
                    baseline_value=previous.control_effectiveness,
                    current_value=current.control_effectiveness
                )
                self.db.add(record)
                drifts.append(record)
                
            if drifts:
                await self.db.commit()
                for d in drifts:
                    await self.db.refresh(d)
                    
        return drifts

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.digital_twin import SimulationResult, OptimizationRecommendation

class OptimizationEngine:
    """
    Identifies failure points in simulations and suggests improvements.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_recommendations(self, result: SimulationResult) -> list[OptimizationRecommendation]:
        recs = []
        
        if result.analyst_utilization_rate > 0.9:
            recs.append(OptimizationRecommendation(
                result_id=result.id,
                category="AUTOMATION",
                title="Deploy Phishing Auto-Remediation Playbook",
                description="Analyst queue is saturated. Automating the top alert category (Phishing) will reduce manual workload by 22%.",
                expected_impact="Reduces utilization by 15%, dropping MTTR by 40 minutes."
            ))
            
            recs.append(OptimizationRecommendation(
                result_id=result.id,
                category="STAFFING",
                title="Hire 2x L1 Analysts",
                description="SLA breach rate is highly sensitive to the current alert volume. Additional headcount is required to restore baseline operations.",
                expected_impact="Restores SLA compliance to 98%."
            ))
            
        for r in recs:
            self.db.add(r)
            
        if recs:
            await self.db.commit()
            
        return recs

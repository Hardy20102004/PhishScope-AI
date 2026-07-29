import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.digital_twin import SimulationScenario, SimulationResult

class SimulationEngine:
    """
    Calculates the mathematical impact of scenario parameters on baseline SOC KPIs.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_scenario(self, scenario: SimulationScenario) -> SimulationResult:
        # Baseline Assumptions
        BASE_MTTR = 30.0 # minutes
        BASE_VOLUME = 1000 # alerts per day
        ALERTS_PER_ANALYST = 50 
        
        # Scenario Adjustments
        projected_volume = BASE_VOLUME * scenario.alert_volume_multiplier
        unautomated_volume = projected_volume * (1.0 - scenario.automation_rate)
        
        # Calculate Utilization
        capacity = scenario.analyst_headcount * ALERTS_PER_ANALYST
        utilization = unautomated_volume / capacity if capacity > 0 else 9.99
        
        # Calculate MTTR & SLA Impacts
        if utilization <= 0.8:
            projected_mttr = BASE_MTTR * 0.9  # Idle time allows faster response
            sla_breach = 0.02
        elif utilization <= 1.0:
            projected_mttr = BASE_MTTR
            sla_breach = 0.05
        else:
            # Queueing theory exponential degradation
            projected_mttr = BASE_MTTR * (utilization ** 2)
            sla_breach = min(1.0, 0.05 * (utilization ** 3))
            
        result = SimulationResult(
            scenario_id=scenario.id,
            forecasted_mttr_mins=projected_mttr,
            forecasted_sla_breach_rate=sla_breach,
            analyst_utilization_rate=utilization
        )
        
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

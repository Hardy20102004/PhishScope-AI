import math

class CapacityEngine:
    """
    Forecasts future analyst headcount requirements.
    """
    def estimate_headcount_needs(self, forecasted_utilization: float, current_headcount: int) -> dict:
        """
        Determines if hiring is needed to maintain < 80% utilization.
        """
        if forecasted_utilization <= 0.8:
            return {"status": "HEALTHY", "suggested_hires": 0}
            
        # Target utilization is 80%
        required_capacity_multiplier = forecasted_utilization / 0.8
        optimal_headcount = math.ceil(current_headcount * required_capacity_multiplier)
        
        return {
            "status": "CRITICAL",
            "suggested_hires": optimal_headcount - current_headcount
        }

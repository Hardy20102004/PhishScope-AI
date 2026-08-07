from sqlalchemy.orm import Session
from app.reputation_engine.models import ReputationProfile, ReputationTrend
from loguru import logger

class TrendAnalysisEngine:
    """
    Analyzes historical scores to determine the reputation trajectory.
    """
    def __init__(self, db: Session):
        self.db = db

    def evaluate_trend(self, profile: ReputationProfile) -> ReputationTrend:
        """
        Calculates if the reputation is improving or declining based on history.
        """
        # In a full implementation, we'd query the `reputation_history` table,
        # calculate moving averages or linear regression slopes.
        # For this prototype, we simulate a basic logic threshold.
        
        logger.info(f"Evaluating trend for {profile.entity_id}")
        
        if profile.risk_score > 80:
            trend = ReputationTrend.DECLINING # Risk is high and getting worse (reputation declining)
        elif profile.trust_score > 80:
            trend = ReputationTrend.IMPROVING
        elif profile.risk_score > 50 and profile.trust_score < 50:
             trend = ReputationTrend.DECLINING
        else:
            trend = ReputationTrend.STABLE
            
        profile.trend = trend
        self.db.commit()
        
        return trend

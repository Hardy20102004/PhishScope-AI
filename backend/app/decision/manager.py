import structlog
from sqlalchemy.orm import Session

from app.decision.confidence import ConfidenceEngine
from app.decision.hypothesis import HypothesisEngine
from app.decision.policy import DecisionPolicyEngine
from app.decision.reasoner import DecisionReasoner
from app.decision.recommendation import RecommendationEngine
from app.models.decision import DecisionEvidenceLink, DecisionRecord
from app.schemas.decision import DecisionCreate

logger = structlog.get_logger("phoenix.decision.manager")

class DecisionManager:
    """Orchestrates the entire decision pipeline."""
    
    def __init__(self, db: Session):
        self.db = db
        self.reasoner = DecisionReasoner()
        self.confidence_engine = ConfidenceEngine()
        self.hypothesis_engine = HypothesisEngine()
        self.policy_engine = DecisionPolicyEngine()
        self.recommendation_engine = RecommendationEngine()

    def evaluate(self, request: DecisionCreate) -> DecisionRecord:
        logger.info("starting_decision_evaluation", type=request.decision_type)
        
        # 1. Reasoning
        reasoning_output = self.reasoner.generate_reasoning(request.decision_type, request.evidence)
        
        # 2. Confidence
        confidence = self.confidence_engine.calculate_confidence(request.decision_type, request.evidence)
        
        # 3. Alternatives
        alternatives = self.hypothesis_engine.generate_alternatives(request.decision_type, reasoning_output["reasoning_chain"])
        
        # 4. Recommendations
        recommendations = self.recommendation_engine.generate_recommendations(request.decision_type, confidence)
        
        # 5. Policy Validation (Determine State)
        final_state = self.policy_engine.validate_decision(recommendations, confidence)
        
        # 6. Save to DB
        record = DecisionRecord(
            decision_type=request.decision_type,
            case_id=request.case_id,
            summary=reasoning_output["summary"],
            confidence=confidence,
            reasoning_chain=reasoning_output["reasoning_chain"],
            assumptions=reasoning_output["assumptions"],
            limitations=reasoning_output["limitations"],
            alternatives=[a.model_dump() for a in alternatives],
            recommendations=[r.model_dump() for r in recommendations],
            state=final_state
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        
        # Save Evidence Links
        for ev in request.evidence:
            link = DecisionEvidenceLink(
                decision_id=record.id,
                source_type=ev.source_type,
                source_id=ev.source_id,
                description=ev.description
            )
            self.db.add(link)
            
        self.db.commit()
        self.db.refresh(record)
        
        logger.info("decision_evaluation_complete", decision_id=record.id, state=record.state)
        return record

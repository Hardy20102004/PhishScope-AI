import structlog
from sqlalchemy.orm import Session
from app.models.decision import DecisionRecord
from app.models.xai import ExplanationRecord, EvidenceAttribution
from app.schemas.xai import ExplanationCreate
from app.xai.attribution import EvidenceAttributionEngine
from app.xai.confidence_explainer import ConfidenceExplanationEngine
from app.xai.feature_importance import FeatureImportanceEngine
from app.xai.narrative import NarrativeGenerator

logger = structlog.get_logger("phoenix.xai.manager")

class ExplanationManager:
    """Orchestrates the XAI Pipeline"""
    
    def __init__(self, db: Session):
        self.db = db
        self.attribution_engine = EvidenceAttributionEngine()
        self.confidence_engine = ConfidenceExplanationEngine()
        self.feature_engine = FeatureImportanceEngine()
        self.narrative_generator = NarrativeGenerator()

    def generate_explanation(self, decision_id: str) -> ExplanationRecord:
        logger.info("starting_xai_generation", decision_id=decision_id)
        
        # 1. Fetch Decision and Evidence
        decision = self.db.query(DecisionRecord).filter_by(id=decision_id).first()
        if not decision:
            raise ValueError("Decision not found")
            
        # Check if explanation already exists
        existing = self.db.query(ExplanationRecord).filter_by(decision_id=decision_id).first()
        if existing:
            return existing

        evidence_links = decision.evidence_links
        
        # 2. Evidence Attribution
        attributions = self.attribution_engine.generate_attributions(evidence_links)
        
        # 3. Confidence Breakdown
        confidence_factors = self.confidence_engine.break_down_confidence(decision.confidence, evidence_links)
        
        # 4. Feature Importance
        feature_ranks = self.feature_engine.generate_feature_ranking(decision.decision_type, evidence_links)
        
        # 5. Narrative Generation
        exec_summary = self.narrative_generator.generate_executive_summary(decision, decision.confidence)
        tech_summary = self.narrative_generator.generate_technical_summary(decision, attributions)
        
        # 6. Save to DB
        record = ExplanationRecord(
            decision_id=decision_id,
            executive_summary=exec_summary,
            technical_summary=tech_summary,
            confidence_breakdown=[f.model_dump() for f in confidence_factors],
            feature_importance=[f.model_dump() for f in feature_ranks]
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        
        # Save Attributions
        for attr in attributions:
            db_attr = EvidenceAttribution(
                explanation_id=record.id,
                evidence_link_id=attr.evidence_link_id,
                importance_weight=attr.importance_weight,
                attribution_text=attr.attribution_text
            )
            self.db.add(db_attr)
            
        self.db.commit()
        self.db.refresh(record)
        
        logger.info("xai_generation_complete", explanation_id=record.id)
        return record

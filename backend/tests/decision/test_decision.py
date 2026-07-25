from app.decision.confidence import ConfidenceEngine
from app.decision.policy import DecisionPolicyEngine
from app.decision.hypothesis import HypothesisEngine
from app.schemas.decision import EvidenceLinkBase, RecommendationItem
from app.models.decision import DecisionState

def test_confidence_engine():
    engine = ConfidenceEngine()
    
    # Empty evidence
    assert engine.calculate_confidence("THREAT_CLASSIFICATION", []) == 0.4
    
    # Dense evidence with KG
    evidence = [
        EvidenceLinkBase(source_type="KNOWLEDGE_GRAPH", source_id="1"),
        EvidenceLinkBase(source_type="RAG_DOCUMENT", source_id="2"),
        EvidenceLinkBase(source_type="RAW_LOG", source_id="3"),
        EvidenceLinkBase(source_type="RAW_LOG", source_id="4"),
        EvidenceLinkBase(source_type="RAW_LOG", source_id="5")
    ]
    score = engine.calculate_confidence("THREAT_CLASSIFICATION", evidence)
    import math
    assert math.isclose(score, 0.9, rel_tol=1e-9) # Base 0.4 + 0.2 (qty) + 0.3 (quality)

def test_policy_engine():
    engine = DecisionPolicyEngine()
    
    recs = [RecommendationItem(action="BLOCK_DOMAIN", priority="HIGH", description="Block")]
    # High impact action always needs review
    assert engine.validate_decision(recs, 0.9) == DecisionState.PENDING_REVIEW
    
def test_hypothesis_engine():
    engine = HypothesisEngine()
    alts = engine.generate_alternatives("THREAT_CLASSIFICATION", [])
    assert len(alts) > 0
    assert alts[0].probability > 0.0

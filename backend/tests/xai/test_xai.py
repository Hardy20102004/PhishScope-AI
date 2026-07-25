from app.xai.attribution import EvidenceAttributionEngine
from app.xai.narrative import NarrativeGenerator


def test_attribution_engine():
    engine = EvidenceAttributionEngine()
    
    class MockLink:
        def __init__(self, t):
            self.id = "mock-id"
            self.source_type = t
            self.source_id = "1"
            
    # Internal KB gets highest weight
    raw = [MockLink("KNOWLEDGE_GRAPH")]
    attr = engine.generate_attributions(raw)
    assert len(attr) == 1
    assert attr[0].importance_weight == 0.9
    
    # OSINT is lower
    raw = [MockLink("RAW_LOG")]
    attr = engine.generate_attributions(raw)
    assert attr[0].importance_weight == 0.5

def test_narrative_generator():
    gen = NarrativeGenerator()
    
    class MockDecision:
        id = "decision-123"
        decision_type = "THREAT_CLASSIFICATION"
        summary = "Malicious file detected."
        recommendations = [{"action": "BLOCK_HASH", "priority": "HIGH"}]
        reasoning_chain = [{"step": 1, "observation": "obs", "inference": "inf"}]
        assumptions = ["assump1"]
        limitations = ["limit1"]
        
    exec_summary = gen.generate_executive_summary(MockDecision(), 0.9)
    assert "High confidence" in exec_summary
    assert "BLOCK_HASH" in exec_summary
    
    class MockAttr:
        attribution_text = "test attribution"
        source_type = "TEST"
        source_id = "1"
        
    tech_summary = gen.generate_technical_summary(MockDecision(), [MockAttr()])
    assert "Reasoning Chain" in tech_summary
    assert "test attribution" in tech_summary

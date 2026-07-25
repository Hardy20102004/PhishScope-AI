import structlog
from typing import Dict, Any

logger = structlog.get_logger("phoenix.xai.narrative")

class NarrativeGenerator:
    """
    Generates human-readable narratives based on the structured decision data.
    """
    def generate_executive_summary(self, decision: Any, confidence: float) -> str:
        logger.info("generating_executive_summary")
        # Template-based generation for local env
        
        confidence_str = "High" if confidence >= 0.8 else "Medium" if confidence >= 0.5 else "Low"
        
        narrative = f"The AI Engine evaluated a {decision.decision_type.replace('_', ' ')} with {confidence_str} confidence ({(confidence * 100):.0f}%).\n\n"
        narrative += f"Summary: {decision.summary}\n\n"
        narrative += "Key Recommendations:\n"
        for rec in decision.recommendations:
            narrative += f"- {rec['action']} (Priority: {rec['priority']})\n"
            
        return narrative

    def generate_technical_summary(self, decision: Any, attributions: list) -> str:
        logger.info("generating_technical_summary")
        
        narrative = f"Technical Analysis for {decision.id}:\n\n"
        narrative += "Reasoning Chain:\n"
        for step in decision.reasoning_chain:
            narrative += f"Step {step['step']}: {step['observation']} -> {step['inference']}\n"
            
        narrative += "\nAssumptions & Limitations:\n"
        for ass in decision.assumptions:
            narrative += f"- Assumption: {ass}\n"
        for lim in decision.limitations:
            narrative += f"- Limitation: {lim}\n"
            
        narrative += "\nPrimary Evidence:\n"
        for att in attributions[:3]: # top 3
            narrative += f"- {att.attribution_text} (Source: {att.source_type}:{att.source_id})\n"
            
        return narrative

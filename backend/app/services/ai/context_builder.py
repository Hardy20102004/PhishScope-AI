import json
from app.models.investigation import Investigation

class ContextBuilder:
    """Builds structured context strings from database records for the LLM."""
    
    @staticmethod
    def build_investigation_context(investigation: Investigation) -> str:
        """Converts investigation data into a readable format for the LLM."""
        
        context_parts = []
        context_parts.append(f"INVESTIGATION TARGET: {investigation.target}")
        context_parts.append(f"INVESTIGATION TYPE: {investigation.type.value if hasattr(investigation.type, 'value') else investigation.type}")
        context_parts.append(f"STATUS: {investigation.status.value if hasattr(investigation.status, 'value') else investigation.status}")
        
        if investigation.risk_score is not None:
            context_parts.append(f"RISK SCORE: {investigation.risk_score}")
        if investigation.risk_level:
            context_parts.append(f"RISK LEVEL: {investigation.risk_level}")
            
        context_parts.append("\n--- EVIDENCE ---")
        if investigation.evidence:
            context_parts.append(json.dumps(investigation.evidence, indent=2))
        else:
            context_parts.append("No evidence collected yet.")
            
        context_parts.append("\n--- FINDINGS ---")
        if investigation.findings:
            context_parts.append(json.dumps(investigation.findings, indent=2))
        else:
            context_parts.append("No findings recorded yet.")
            
        return "\n".join(context_parts)

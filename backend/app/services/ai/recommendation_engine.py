import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.investigation import Investigation
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.llm_service import MockLLMService
from app.services.ai.prompt_manager import PromptManager


class RecommendationEngine:
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = MockLLMService()
        
    async def get_recommendations(self, investigation_id: uuid.UUID) -> List[str]:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        investigation = self.db.execute(stmt).scalar_one_or_none()
        if not investigation:
            raise ValueError("Investigation not found")
            
        context = ContextBuilder.build_investigation_context(investigation)
        
        # We simulate the LLM returning a JSON array of suggestions
        # In a real scenario we'd parse the LLM's string output to JSON
        # For the mock, we can just return static ones or use a trick
        
        response = await self.llm_service.generate_response(
            system_prompt=PromptManager.RECOMMENDATION_PROMPT,
            messages=[{"role": "user", "content": "What should I do next?"}],
            context=context
        )
        
        # Simulated fallback for mock
        return [
            "Extract all IP addresses from the HTML source and run Threat Intel checks.",
            "Verify the WHOIS registration date of the domain.",
            "Check if the TLS certificate is shared across other known malicious domains."
        ]

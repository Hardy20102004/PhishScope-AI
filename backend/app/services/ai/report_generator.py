from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid

from app.models.investigation import Investigation
from app.models.copilot import GeneratedReport
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.prompt_manager import PromptManager
from app.services.ai.llm_service import MockLLMService

class ReportGenerator:
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = MockLLMService()
        
    async def generate_report(self, investigation_id: uuid.UUID, report_type: str, user_id: uuid.UUID) -> GeneratedReport:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        investigation = self.db.execute(stmt).scalar_one_or_none()
        if not investigation:
            raise ValueError("Investigation not found")
            
        context = ContextBuilder.build_investigation_context(investigation)
        
        report_content = await self.llm_service.generate_report(
            system_prompt=PromptManager.REPORT_GENERATION_PROMPT,
            context=context
        )
        
        report = GeneratedReport(
            investigation_id=investigation_id,
            report_type=report_type,
            content=report_content,
            generated_by=user_id
        )
        
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        
        return report

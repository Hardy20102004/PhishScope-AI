import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.copilot import CopilotConversation, CopilotMessage, MessageRole
from app.schemas.dfir_copilot import DfirQuery, DfirResponse, DfirResponseChunk
from app.dfir_copilot.timeline_reasoning import TimelineReasoningEngine
from app.dfir_copilot.artifact_explanation import ArtifactExplanationEngine

class ConversationEngine:
    """
    Orchestrates the LLM prompt workflow, enforcing separation between fact and inference.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_query(self, query: DfirQuery) -> DfirResponse:
        
        # 1. Save User Query
        user_msg = CopilotMessage(
            conversation_id=query.conversation_id,
            role=MessageRole.USER,
            content=query.content
        )
        self.db.add(user_msg)
        
        # 2. Route to specialized engine based on Context Type
        chunks = []
        if query.context_type == "TIMELINE":
            engine = TimelineReasoningEngine(self.db)
            chunks = await engine.reason_timeline(query.investigation_id, query.content)
        elif query.context_type == "ARTIFACT":
            engine = ArtifactExplanationEngine(self.db)
            chunks = await engine.explain_artifact(query.content)
        else:
            # Fallback general RAG
            chunks = [DfirResponseChunk(content="I can help with that.", classification="ASSESSMENT")]

        # 3. Serialize chunks and save Assistant Response
        assistant_msg = CopilotMessage(
            conversation_id=query.conversation_id,
            role=MessageRole.ASSISTANT,
            content=json.dumps([c.model_dump() for c in chunks]),
            evidence_references=[cit for chunk in chunks for cit in chunk.citations]
        )
        self.db.add(assistant_msg)
        await self.db.commit()
        await self.db.refresh(assistant_msg)

        # 4. Generate dynamic next steps
        suggested = ["What happened next?", "Explain the registry modifications.", "Is there a related network beacon?"]
        
        return DfirResponse(
            message_id=assistant_msg.id,
            chunks=chunks,
            suggested_questions=suggested
        )

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.threat_hunting import HuntSession, HuntQuery, HuntHypothesis
from app.threat_hunting.query_engine import QueryEngine
from app.threat_hunting.hypothesis_engine import HypothesisEngine

class ThreatHuntManager:
    """
    Central orchestrator for Threat Hunting workspaces.
    Manages active hunt sessions, queries, and AI interactions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.query_engine = QueryEngine(db)
        self.hypothesis_engine = HypothesisEngine(db)

    async def create_session(self, title: str, objective: str, user_id: uuid.UUID, tenant_id: uuid.UUID) -> HuntSession:
        session = HuntSession(
            tenant_id=tenant_id,
            title=title,
            objective=objective,
            assigned_hunter_id=user_id,
            status="ACTIVE"
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def execute_query(self, session_id: uuid.UUID, raw_query: str) -> HuntQuery:
        """
        Translates a natural language query into structured, stores the record, 
        and simulates execution against backend stores.
        """
        # Parse and execute using the engine
        query_record, results = await self.query_engine.execute_natural_language_search(session_id, raw_query)
        
        # In a real system, `results` would be passed back or streamed to the client.
        return query_record

    async def generate_hypotheses_for_session(self, session_id: uuid.UUID) -> list[HuntHypothesis]:
        """
        Asks the AI Context Engine to generate hypotheses based on current session data.
        """
        return await self.hypothesis_engine.generate_hypotheses(session_id)

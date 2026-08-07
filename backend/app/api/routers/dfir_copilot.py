from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.dfir_copilot import DfirQuery, DfirResponse
from app.dfir_copilot.conversation_engine import ConversationEngine

router = APIRouter()

@router.post("/chat", response_model=DfirResponse, status_code=status.HTTP_200_OK)
async def chat_with_copilot(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    query_in: DfirQuery,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submits a natural language query to the DFIR Copilot.
    The response explicitly separates Observations, Assessments, and Recommendations.
    """
    engine = ConversationEngine(db)
    response = await engine.process_query(query_in)
    return response

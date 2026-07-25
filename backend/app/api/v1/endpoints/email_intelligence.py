from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.email_intelligence.orchestrator import EmailInvestigationOrchestrator

router = APIRouter()

class EmailSubmission(BaseModel):
    raw_eml: str

class EmailInvestigationResponse(BaseModel):
    header_data: Dict[str, Any]
    auth_results: Dict[str, Any]
    routing_hops: list
    conversation_analysis: Dict[str, Any]
    attachments: list
    campaign_correlation: Dict[str, Any]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=EmailInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_email(submission: EmailSubmission):
    """
    Submits a raw RFC 5322 email string for deep Email investigation.
    """
    try:
        results = await EmailInvestigationOrchestrator.run_investigation(submission.raw_eml)
        if "error" in results:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to parse email: {results['error']}"
            )
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to investigate email: {str(e)}"
        )

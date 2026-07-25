from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any

from app.url_intelligence.orchestrator import InvestigationOrchestrator

router = APIRouter()

class URLSubmission(BaseModel):
    url: str

class URLInvestigationResponse(BaseModel):
    canonical_url: str
    parsed: Dict[str, Any]
    intelligence: Dict[str, Any]
    redirect_chain: list
    infrastructure: Dict[str, Any]
    brand: Dict[str, Any]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=URLInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_url(submission: URLSubmission):
    """
    Submits a URL for deep intelligence investigation.
    Returns parsed data, redirect chains, infrastructure correlation, brand similarity, and AI narrative.
    """
    try:
        results = await InvestigationOrchestrator.run_investigation(submission.url)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to investigate URL: {str(e)}"
        )

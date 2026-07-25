from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List

from app.browser_investigation.orchestrator import BrowserInvestigationManager

router = APIRouter()

class BrowserSubmission(BaseModel):
    export_payload: str

class BrowserInvestigationResponse(BaseModel):
    history: List[Dict[str, Any]]
    cookies: List[Dict[str, Any]]
    extensions: List[Dict[str, Any]]
    downloads: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    iocs: List[Dict[str, str]]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=BrowserInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_browser(submission: BrowserSubmission):
    """
    Submits a mock forensic browser backup payload for processing.
    """
    try:
        results = await BrowserInvestigationManager.run_investigation(submission.export_payload)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process browser forensics data: {str(e)}"
        )

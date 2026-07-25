from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from app.website_investigation.orchestrator import WebsiteInvestigationOrchestrator

router = APIRouter()

class WebsiteSubmission(BaseModel):
    url: str

class WebsiteInvestigationResponse(BaseModel):
    url: str
    snapshot_metadata: Dict[str, Any]
    html_analysis: Dict[str, Any]
    javascript_analysis: list
    form_analysis: list
    cookie_analysis: Dict[str, Any]
    security_headers: Dict[str, Any]
    visual_analysis: Dict[str, Any]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=WebsiteInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_website(submission: WebsiteSubmission):
    """
    Submits a URL for deep Website investigation (HTML, JS, DOM, Visuals).
    """
    try:
        results = await WebsiteInvestigationOrchestrator.run_investigation(submission.url)
        if "error" in results:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch website: {results['error']}"
            )
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to investigate website: {str(e)}"
        )

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List

from app.mobile_investigation.orchestrator import MobileInvestigationManager

router = APIRouter()

class MobileSubmission(BaseModel):
    export_payload: str

class MobileInvestigationResponse(BaseModel):
    device_metadata: Dict[str, Any]
    applications: List[Dict[str, Any]]
    communications: List[Dict[str, Any]]
    locations: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    iocs: List[Dict[str, str]]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=MobileInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_mobile(submission: MobileSubmission):
    """
    Submits a mock forensic backup payload for processing.
    In a full implementation, this would accept large JSON/XML/SQLite files via multipart/form-data.
    """
    try:
        results = await MobileInvestigationManager.run_investigation(submission.export_payload)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process mobile forensics data: {str(e)}"
        )

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.cloud_investigation.orchestrator import CloudInvestigationManager

router = APIRouter()

class CloudSubmission(BaseModel):
    export_payload: str

class CloudInvestigationResponse(BaseModel):
    assets: List[Dict[str, Any]]
    identities: List[Dict[str, Any]]
    configurations: List[Dict[str, Any]]
    audit_logs: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    iocs: List[Dict[str, str]]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=CloudInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_cloud(submission: CloudSubmission):
    """
    Submits a mock cloud forensic payload (JSON) for processing.
    """
    try:
        results = await CloudInvestigationManager.run_investigation(submission.export_payload)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process cloud forensics data: {str(e)}"
        )

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List

from app.network_investigation.orchestrator import NetworkInvestigationManager

router = APIRouter()

class NetworkSubmission(BaseModel):
    export_payload: str

class NetworkInvestigationResponse(BaseModel):
    flows: List[Dict[str, Any]]
    dns: List[Dict[str, Any]]
    http: List[Dict[str, Any]]
    tls: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    iocs: List[Dict[str, str]]
    risk_score: Dict[str, Any]
    ai_summary: Dict[str, str]

@router.post("/investigate", response_model=NetworkInvestigationResponse, status_code=status.HTTP_200_OK)
async def investigate_network(submission: NetworkSubmission):
    """
    Submits a mock forensic network capture payload (Zeek JSON) for processing.
    """
    try:
        results = await NetworkInvestigationManager.run_investigation(submission.export_payload)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process network forensics data: {str(e)}"
        )
